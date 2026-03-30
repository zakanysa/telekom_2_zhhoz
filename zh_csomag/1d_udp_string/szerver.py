"""
1. feladat – UDP SZERVER, d) variáns
--------------------------------------
Ugyanaz a logika mint a TCP szerver, de UDP-vel (SOCK_DGRAM).
Fogadja a (20s i) struct-ot, visszaküldi az első X karakter fordítottját.
"""

import socket
import struct

recv_packer = struct.Struct('20s i')
SERVER_ADDR = ('localhost', 10000)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(SERVER_ADDR)
    server.settimeout(1.0)
    print(f'UDP szerver figyel: {SERVER_ADDR}')

    while True:
        try:
            # recvfrom: visszaadja az adatot ÉS a feladó (kliens) címét
            data, client_addr = server.recvfrom(recv_packer.size)

            raw_text, number = recv_packer.unpack(data)
            text = raw_text.decode().strip('\x00')
            print(f'Kapott: "{text}", szám: {number} tőle: {client_addr}')

            result = text[:number][::-1]
            print(f'Visszaküld: "{result}"')

            # sendto: adat + célcím (a kliens visszacíme)
            server.sendto(result.encode(), client_addr)

        except socket.timeout:
            pass
        except KeyboardInterrupt:
            print('Szerver leáll.')
            break
