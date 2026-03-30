"""
1. feladat – TCP KLIENS, b) variáns
-------------------------------------
Betölti az input.txt fájlt (soronként: "szöveg szám"),
véletlen számmal (1-3) kiválaszt egy sort, elküldi struct-ban (20s i).

input.txt:
almafa 4
kortefa 3
barackfa 5
"""

import socket
import struct
import random

packer = struct.Struct('20s i')
SERVER_ADDR = ('localhost', 10000)

# TXT beolvasás
with open('input.txt', 'r') as f:
    lines = f.readlines()           # ['almafa 4\n', 'kortefa 3\n', ...]

rand_idx = random.randint(1, 3)     # 1, 2 vagy 3
line     = lines[rand_idx - 1].strip()   # 0-indexelt lista!
print(f'Kiválasztott sor #{rand_idx}: "{line}"')

parts  = line.split()
text   = parts[0]                   # "almafa"
number = int(parts[1])              # 4

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(SERVER_ADDR)
    sock.sendall(packer.pack(text.encode(), number))
    print(f'Elküldve: "{text}", szám: {number}')

    raw = sock.recv(1024)
    print(f'Szerver válasza: "{raw.decode().strip(chr(0))}"')
