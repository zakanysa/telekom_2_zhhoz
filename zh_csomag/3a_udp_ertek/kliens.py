"""
3. feladat a) – UDP KLIENS
-----------------------------
PUSH/PLUS/MINUS parancsokat küld (5s i) struct-ban az UDP szervernek.
A válasz (i) struct – kicsomagolni kell, nem decode()!
"""

import socket
import struct

send_packer = struct.Struct('5s i')   # küldés
recv_packer = struct.Struct('i')      # fogadás (válasz)
SERVER_ADDR = ('localhost', 10001)

def kuldd(sock, cmd: str, value: int):
    """Elküldi a parancsot és kiírja a szerver válaszát."""
    # A cmd-et pontosan 5 bájtosra paddingoljuk
    packed = send_packer.pack(cmd.encode().ljust(5), value)
    sock.sendto(packed, SERVER_ADDR)

    data, _ = sock.recvfrom(recv_packer.size)
    (result,) = recv_packer.unpack(data)   # tuple-ból kicsomagolás!
    print(f'  {cmd} {value:>3}  ->  szerver értéke: {result}')
    return result

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.settimeout(2.0)

    kuldd(sock, 'PUSH',  10)   # érték = 10
    kuldd(sock, 'PLUS',   5)   # 10 + 5 = 15
    kuldd(sock, 'MINUS',  3)   # 15 - 3 = 12
    kuldd(sock, 'PLUS',   0)   # 12 + 0 = 12  (lekérdezés, nem változtat)
