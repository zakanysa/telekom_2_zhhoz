"""
1. feladat – TCP SZERVER (a/b/c variánshoz közös)
---------------------------------------------------
Fogadja a (20s i) struct-ot: szöveg + X szám.
Visszaküldi: szöveg első X karakterét megfordítva.

Példa: "almafa", 4 -> "alma"[::-1] = "amla"
"""

import socket
import struct

recv_packer = struct.Struct('20s i')
SERVER_ADDR = ('localhost', 10000)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(SERVER_ADDR)
    server.listen(5)
    print(f'TCP szerver figyel: {SERVER_ADDR}')

    while True:
        conn, addr = server.accept()
        print(f'Kapcsolódott: {addr}')
        with conn:
            data = conn.recv(recv_packer.size)
            if not data:
                continue

            raw_text, number = recv_packer.unpack(data)
            text = raw_text.decode().strip('\x00')
            print(f'Kapott: "{text}", szám: {number}')

            # Első X karakter, megfordítva
            result = text[:number][::-1]
            print(f'Visszaküld: "{result}"')

            conn.sendall(result.encode())
