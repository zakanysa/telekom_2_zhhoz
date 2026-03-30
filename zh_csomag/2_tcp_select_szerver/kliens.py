"""
2. feladat – TCP KLIENS a select-es szerverhez
------------------------------------------------
(4s i) struct-ban küldi a parancsokat.
A string-et pontosan 4 bájtosra kell paddingolni!
  'IN'   -> b'IN  '  (2 szóköz)
  'INCR' -> b'INCR'  (4 karakter, pont jó)
  'DECR' -> b'DECR'
"""

import socket
import struct

cmd_packer  = struct.Struct('4s i')
SERVER_ADDR = ('localhost', 10000)

def kuldd_parancsot(sock, cmd: str, value: int):
    """Elküldi a parancsot és kiírja a szerver válaszát."""
    # ljust(4): jobbra paddingol szóközzel ha rövidebb mint 4 karakter
    packed = cmd_packer.pack(cmd.encode().ljust(4), value)
    sock.sendall(packed)
    response = sock.recv(1024).decode()
    print(f'  {cmd} {value:>3}  ->  szerver értéke: {response}')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(SERVER_ADDR)
    print(f'Kapcsolódva: {SERVER_ADDR}')

    kuldd_parancsot(sock, 'IN',   20)   # érték = 20
    kuldd_parancsot(sock, 'INCR',  4)   # 20 + 4 = 24
    kuldd_parancsot(sock, 'DECR',  5)   # 24 - 5 = 19
    kuldd_parancsot(sock, 'INCR',  0)   # 19 + 0 = 19  (lekérdezés)
