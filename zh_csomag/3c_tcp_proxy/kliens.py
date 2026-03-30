"""
3. feladat c) – TCP KLIENS (a proxy-hoz csatlakozik)
------------------------------------------------------
Ugyanaz mint a 2. feladat kliens – IN/INCR/DECR parancsokat küld (4s i).
A különbség: a szerver valójában proxy, az értéket az UDP szerver tárolja.
A kliens ezt NEM TUDJA, számára átlátszó.
"""

import socket
import struct

cmd_packer  = struct.Struct('4s i')
SERVER_ADDR = ('localhost', 10000)   # a proxy címe

def kuldd(sock, cmd: str, value: int):
    packed = cmd_packer.pack(cmd.encode().ljust(4), value)
    sock.sendall(packed)
    response = sock.recv(1024).decode()
    print(f'  {cmd} {value:>3}  ->  szerver értéke: {response}')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(SERVER_ADDR)
    print(f'Kapcsolódva a proxyhoz: {SERVER_ADDR}')

    kuldd(sock, 'IN',   20)    # érték = 20
    kuldd(sock, 'INCR',  4)    # 20 + 4 = 24
    kuldd(sock, 'DECR',  5)    # 24 - 5 = 19
