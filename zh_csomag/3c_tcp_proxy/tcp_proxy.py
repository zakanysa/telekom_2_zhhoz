"""
3. feladat c) – TCP PROXY SZERVER
-----------------------------------
A TCP kliensek (4s i) formátumban küldnek parancsokat.
A proxy konvertálja a parancsneveket és UDP-n továbbítja az UDP szervernek (5s i).
Az UDP szerver struct (i) válaszát bytesztringként adja vissza a TCP kliensnek.

Konverzió:
  TCP: IN   -> UDP: PUSH
  TCP: INCR -> UDP: PLUS
  TCP: DECR -> UDP: MINUS

Indítási sorrend: 1. udp_szerver.py  2. tcp_proxy.py  3. kliens.py
"""

import socket
import select
import struct

# TCP oldal (kliensek ide csatlakoznak)
TCP_ADDR    = ('localhost', 10000)
tcp_packer  = struct.Struct('4s i')

# UDP oldal (ide továbbítunk)
UDP_ADDR    = ('localhost', 10001)
udp_send    = struct.Struct('5s i')
udp_recv    = struct.Struct('i')

# Parancs konverzió táblázat (pontosan 5 bájt!)
CMD_MAP = {
    'IN':   b'PUSH ',
    'INCR': b'PLUS ',
    'DECR': b'MINUS',
}

def udp_forward(cmd: str, value: int) -> int:
    """Parancsot küld UDP-n, visszaadja az UDP szerver válaszát."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
        udp.settimeout(2.0)
        udp.sendto(udp_send.pack(CMD_MAP[cmd], value), UDP_ADDR)
        data, _ = udp.recvfrom(udp_recv.size)
        (result,) = udp_recv.unpack(data)
        return result

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.setblocking(False)
    server.bind(TCP_ADDR)
    server.listen(5)
    print(f'TCP proxy figyel: {TCP_ADDR}  ->  UDP: {UDP_ADDR}')

    inputs = [server]

    while inputs:
        readable, _, _ = select.select(inputs, [], [], 1)

        for sock in readable:
            if sock is server:
                conn, addr = server.accept()
                conn.setblocking(False)
                inputs.append(conn)
                print(f'Új TCP kliens: {addr}')
            else:
                data = sock.recv(tcp_packer.size)
                if not data:
                    print(f'TCP kliens kilépett: {sock.getpeername()}')
                    inputs.remove(sock)
                    sock.close()
                else:
                    cmd_raw, value = tcp_packer.unpack(data)
                    cmd = cmd_raw.decode().strip()
                    print(f'[PROXY] TCP parancs: "{cmd}" {value}  -> UDP...')

                    result = udp_forward(cmd, value)
                    print(f'[PROXY] UDP válasz: {result}  -> TCP kliensnek')

                    sock.sendall(str(result).encode())
