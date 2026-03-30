"""
3. feladat c) – UDP SZERVER (a 3a szerverrel azonos)
-----------------------------------------------------
Ez a tényleges adattároló. A TCP proxy ide továbbítja a parancsokat.
Parancsok: PUSH/PLUS/MINUS (5s i), válasz: (i) struct.
"""

import socket
import struct

recv_packer  = struct.Struct('5s i')
resp_packer  = struct.Struct('i')
SERVER_ADDR  = ('localhost', 10001)
stored_value = 0

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(SERVER_ADDR)
    sock.settimeout(1.0)
    print(f'UDP szerver figyel: {SERVER_ADDR}')

    while True:
        try:
            data, client_addr = sock.recvfrom(recv_packer.size)

            cmd_raw, value = recv_packer.unpack(data)
            cmd = cmd_raw.decode().strip()

            if cmd == 'PUSH':
                stored_value = value
            elif cmd == 'PLUS':
                stored_value += value
            elif cmd == 'MINUS':
                stored_value -= value

            print(f'[UDP] "{cmd}" {value}  -> tárolt: {stored_value}')
            sock.sendto(resp_packer.pack(stored_value), client_addr)

        except socket.timeout:
            pass
        except KeyboardInterrupt:
            break
