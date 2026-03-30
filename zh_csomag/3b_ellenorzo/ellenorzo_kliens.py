"""
3. feladat b) – ELLENŐRZŐ KLIENS
----------------------------------
Mindkét szervertől lekérdezi a tárolt értéket "0-val való növelés" küldésével,
összehasonlítja, és megállapítja, hibázott-e az UDP szerver.

TCP lekérdezés:  INCR 0  (érték nem változik, visszakapjuk a jelenlegi értéket)
UDP lekérdezés:  PLUS 0  (ugyanez UDP-n, de a szerver +-1-et adhat hozzá)
"""

import socket
import struct

TCP_ADDR = ('localhost', 10000)
UDP_ADDR = ('localhost', 10001)

tcp_packer  = struct.Struct('4s i')
udp_send    = struct.Struct('5s i')
udp_recv    = struct.Struct('i')

def kerdezes_tcp() -> int:
    """INCR 0 küldése TCP-n -> visszakapja a tárolt értéket."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(TCP_ADDR)
        sock.sendall(tcp_packer.pack(b'INCR', 0))
        return int(sock.recv(1024).decode())

def kerdezes_udp() -> int:
    """PLUS 0 küldése UDP-n -> visszakapja a tárolt értéket (esetleg hibával)."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(2.0)
        sock.sendto(udp_send.pack(b'PLUS ', 0), UDP_ADDR)
        data, _ = sock.recvfrom(udp_recv.size)
        (value,) = udp_recv.unpack(data)   # tuple-ból int kicsomagolás
        return value

tcp_ertek = kerdezes_tcp()
udp_ertek = kerdezes_udp()

print(f'TCP szerver értéke: {tcp_ertek}')
print(f'UDP szerver értéke: {udp_ertek}')

if tcp_ertek == udp_ertek:
    print('Az UDP szerver NEM hibázott.')
else:
    diff = udp_ertek - tcp_ertek
    print(f'Az UDP szerver HIBÁZOTT! Eltérés: {diff:+d}')
