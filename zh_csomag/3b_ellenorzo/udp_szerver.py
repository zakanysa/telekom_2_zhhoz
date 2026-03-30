"""
3. feladat b) – UDP SZERVER (hibázó verzió)
--------------------------------------------
A 3a szerverrel azonos, de minden parancs feldolgozásakor
véletlenszerűen -1, 0 vagy +1-et ad a számhoz (szimulált hiba).
Az ellenőrző kliens PLUS 0-t küld ide a lekérdezéshez.
"""

import socket
import struct
import random

recv_packer  = struct.Struct('5s i')
resp_packer  = struct.Struct('i')
SERVER_ADDR  = ('localhost', 10001)
stored_value = 0

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(SERVER_ADDR)
    sock.settimeout(1.0)
    print(f'UDP szerver (hibázó) figyel: {SERVER_ADDR}')

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

            # Véletlenszerű hiba: -1, 0 vagy +1
            hiba = random.choice([-1, 0, 1])
            stored_value += hiba
            if hiba != 0:
                print(f'[UDP] Hiba! {hiba:+d} hozzáadva.')

            print(f'[UDP] "{cmd}" {value}  -> tárolt: {stored_value}')
            sock.sendto(resp_packer.pack(stored_value), client_addr)

        except socket.timeout:
            pass
        except KeyboardInterrupt:
            break
