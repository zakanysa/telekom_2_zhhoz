"""
3. feladat a) – UDP SZERVER
-----------------------------
Tárol egy egész számot (kezdőérték: 0).
Parancsok (5s i) struct formátumban:
  b'PUSH ' + X  -> érték = X
  b'PLUS ' + X  -> érték += X
  b'MINUS' + X  -> érték -= X
Válasz: struct (i) formátumban – NEM sima string, hanem becsomagolt int!
"""

import socket
import struct

recv_packer = struct.Struct('5s i')   # parancs fogadás
resp_packer = struct.Struct('i')      # válasz küldés
SERVER_ADDR = ('localhost', 10001)
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
            print(f'Parancs: "{cmd}" {value} tőle: {client_addr}')

            if cmd == 'PUSH':
                stored_value = value
            elif cmd == 'PLUS':
                stored_value += value
            elif cmd == 'MINUS':
                stored_value -= value

            print(f'Tárolt érték: {stored_value}')

            # Válasz: struct (i) – becsomagolt int, nem string!
            sock.sendto(resp_packer.pack(stored_value), client_addr)

        except socket.timeout:
            pass
        except KeyboardInterrupt:
            print('UDP szerver leáll.')
            break
