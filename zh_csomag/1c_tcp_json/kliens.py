"""
1. feladat – TCP KLIENS, c) variáns
-------------------------------------
Betölti az input.json fájlt, véletlen kulcsot generál (1-3),
str-ré alakítja (JSON kulcs string!), kinyeri a szöveget és a számot,
elküldi struct-ban (20s i).

input.json:
{
  "1": ["almafa", 4],
  "2": ["kortefa", 3],
  "3": ["barackfa", 5]
}
"""

import socket
import struct
import random
import json

packer = struct.Struct('20s i')
SERVER_ADDR = ('localhost', 10000)

# JSON beolvasás
with open('input.json', 'r') as f:
    data_dict = json.load(f)        # {"1": ["almafa", 4], ...}

rand_key = str(random.randint(1, 3))   # int -> str, mert a JSON kulcs string!
print(f'Kiválasztott kulcs: "{rand_key}"')

entry  = data_dict[rand_key]       # ["almafa", 4]
text   = entry[0]                  # "almafa"
number = entry[1]                  # 4

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(SERVER_ADDR)
    sock.sendall(packer.pack(text.encode(), number))
    print(f'Elküldve: "{text}", szám: {number}')

    raw = sock.recv(1024)
    print(f'Szerver válasza: "{raw.decode().strip(chr(0))}"')
