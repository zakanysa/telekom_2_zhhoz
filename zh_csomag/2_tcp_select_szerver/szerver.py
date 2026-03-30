"""
2. feladat – TCP SZERVER select()-tel (több kliens egyszerre)
--------------------------------------------------------------
Tárol egy egész számot (kezdőérték: 0).
Parancsok (4s i) struct formátumban:
  b'IN  ' + X  -> érték = X
  b'INCR' + X  -> érték += X
  b'DECR' + X  -> érték -= X
Minden parancs után visszaküldi az aktuális értéket bytesztringként.
"""

import socket
import select
import struct

cmd_packer  = struct.Struct('4s i')
SERVER_ADDR = ('localhost', 10000)
stored_value = 0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.setblocking(False)   # select() megköveteli a non-blocking módot
    server.bind(SERVER_ADDR)
    server.listen(5)
    print(f'TCP szerver figyel: {SERVER_ADDR}')

    inputs = [server]   # figyelt socketok listája

    while inputs:
        # select(olvasható, írható, hibás, timeout)
        readable, _, _ = select.select(inputs, [], [], 1)

        for sock in readable:
            if sock is server:
                # Új kliens csatlakozott
                conn, addr = server.accept()
                conn.setblocking(False)
                inputs.append(conn)
                print(f'Új kliens: {addr}')
            else:
                data = sock.recv(cmd_packer.size)
                if not data:
                    # Kliens bontotta a kapcsolatot
                    print(f'Kliens kilépett: {sock.getpeername()}')
                    inputs.remove(sock)
                    sock.close()
                else:
                    cmd_raw, value = cmd_packer.unpack(data)
                    cmd = cmd_raw.decode().strip()
                    print(f'Parancs: "{cmd}" {value}')

                    if cmd == 'IN':
                        stored_value = value
                    elif cmd == 'INCR':
                        stored_value += value
                    elif cmd == 'DECR':
                        stored_value -= value

                    print(f'Tárolt érték: {stored_value}')
                    # Visszaküldés bytesztringként (nem struct!)
                    sock.sendall(str(stored_value).encode())
