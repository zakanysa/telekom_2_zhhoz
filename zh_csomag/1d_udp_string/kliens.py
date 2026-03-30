"""
1. feladat – UDP KLIENS, d) variáns
--------------------------------------
Ugyanaz mint az a) variáns, de UDP-vel.
UDP-nél: sendto(adat, cím) + recvfrom(bufméret) -> (adat, cím)
Nincs connect(), nincs sendall().
"""

import socket
import struct
import random

packer = struct.Struct('20s i')
SERVER_ADDR = ('localhost', 10000)

text   = input('Add meg a szöveget: ')
number = random.randint(1, 10)
print(f'Generált szám: {number}')

# UDP socket: SOCK_DGRAM (nem SOCK_STREAM!)
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    data = packer.pack(text.encode(), number)

    # sendto: egyszerre adjuk meg az adatot és a célcímet
    sock.sendto(data, SERVER_ADDR)
    print(f'Elküldve UDP-n: "{text}", szám: {number}')

    # recvfrom: visszaadja az adatot ÉS a feladó (szerver) címét
    raw, server_addr = sock.recvfrom(1024)
    print(f'Szerver válasza ({server_addr}): "{raw.decode().strip(chr(0))}"')
