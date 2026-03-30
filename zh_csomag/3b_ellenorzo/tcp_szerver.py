"""
3. feladat b) – TCP SZERVER (a 2. feladatból, változatlan)
------------------------------------------------------------
Tárol egy egész számot. Parancsok: IN/INCR/DECR (4s i struct).
Válasz: bytesztring (str(ertek).encode()).
Az ellenőrző kliens INCR 0-t küld ide a lekérdezéshez.
"""

import socket
import select
import struct

cmd_packer   = struct.Struct('4s i')
SERVER_ADDR  = ('localhost', 10000)
stored_value = 0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.setblocking(False)
    server.bind(SERVER_ADDR)
    server.listen(5)
    print(f'TCP szerver figyel: {SERVER_ADDR}')

    inputs = [server]

    while inputs:
        readable, _, _ = select.select(inputs, [], [], 1)
        for sock in readable:
            if sock is server:
                conn, addr = server.accept()
                conn.setblocking(False)
                inputs.append(conn)
                print(f'Új kliens: {addr}')
            else:
                data = sock.recv(cmd_packer.size)
                if not data:
                    inputs.remove(sock)
                    sock.close()
                else:
                    cmd_raw, value = cmd_packer.unpack(data)
                    cmd = cmd_raw.decode().strip()
                    if cmd == 'IN':
                        stored_value = value
                    elif cmd == 'INCR':
                        stored_value += value
                    elif cmd == 'DECR':
                        stored_value -= value
                    print(f'[TCP] "{cmd}" {value}  -> tárolt: {stored_value}')
                    sock.sendall(str(stored_value).encode())
