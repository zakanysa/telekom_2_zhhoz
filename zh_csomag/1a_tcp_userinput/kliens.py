"""
1. feladat – TCP KLIENS, a) variáns
-------------------------------------
Bekéri a szöveget a felhasználótól, véletlen számot generál,
(20s i) struct-ban elküldi a szervernek, kiírja a választ.
"""

import socket
import struct
import random

packer = struct.Struct('20s i')
SERVER_ADDR = ('localhost', 10000)

text   = input('Add meg a szöveget: ')       # pl. "almafa"
number = random.randint(1, 10)
print(f'Generált szám: {number}')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(SERVER_ADDR)
    sock.sendall(packer.pack(text.encode(), number))
    print(f'Elküldve: "{text}", szám: {number}')

    raw = sock.recv(1024)
    print(f'Szerver válasza: "{raw.decode().strip(chr(0))}"')
