# Telekommunikáció ZH – Cheat Sheet

## Tartalom
1. [Socket alapok](#1-socket-alapok)
2. [Struct csomagolás](#2-struct-csomagolás)
3. [TCP szerver – egy kliens](#3-tcp-szerver--egy-kliens)
4. [TCP kliens](#4-tcp-kliens)
5. [UDP szerver](#5-udp-szerver)
6. [UDP kliens](#6-udp-kliens)
7. [TCP szerver – több kliens (select)](#7-tcp-szerver--több-kliens-select)
8. [Fájl beolvasás (TXT + JSON)](#8-fájl-beolvasás-txt--json)
9. [Proxy minta (TCP → UDP)](#9-proxy-minta-tcp--udp)
10. [UDP fájlátvitel](#10-udp-fájlátvitel)
11. [Tipikus hibák és javításuk](#11-tipikus-hibák-és-javításuk)
12. [Struct formátumok referencia](#12-struct-formátumok-referencia)

---

## 1. Socket alapok

| Fogalom | Leírás |
|---------|--------|
| `AF_INET` | IPv4 protokoll |
| `SOCK_STREAM` | TCP (kapcsolatorientált, megbízható) |
| `SOCK_DGRAM` | UDP (kapcsolat nélküli, nem megbízható) |
| `SO_REUSEADDR` | Port újrahasználat (szervereknél mindig!) |

```python
import socket

# TCP socket létrehozása
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# UDP socket létrehozása
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Context manager (automatikusan zárja): ajánlott!
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    ...
```

---

## 2. Struct csomagolás

```python
import struct

# Formátum definiálása
packer = struct.Struct('20s i')   # 20 bájtos string + 4 bájtos int

# Csomagolás (bytes-ba)
data = packer.pack(text.encode(), number)

# Kicsomagolás (bytes-ból)
text_raw, number = packer.unpack(data)
text = text_raw.decode().strip('\x00')   # null-bájtok eltávolítása!

# Méret lekérdezése (recv-hez hasznos)
packer.size   # pontosan ennyi bájtot kell olvasni
```

### Formátum karakterek
| Karakter | Típus | Méret |
|----------|-------|-------|
| `s` | bytes (pl. `20s` = 20 bájt) | N bájt |
| `i` | int (előjeles) | 4 bájt |
| `I` | int (előjel nélküli) | 4 bájt |
| `f` | float | 4 bájt |
| `c` | 1 bájtos char | 1 bájt |

> **Fontos:** `b'IN  '` – a string-et pontosan ki kell tölteni! Pl. `'IN'.encode().ljust(4)` vagy `b'IN  '`

---

## 3. TCP szerver – egy kliens

```python
import socket

SERVER_ADDR = ('localhost', 10000)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # MINDIG!
    server.bind(SERVER_ADDR)
    server.listen(5)   # max. 5 várakozó kapcsolat

    while True:
        conn, addr = server.accept()    # blokkoló, megvárja a klienst
        with conn:
            data = conn.recv(1024)      # fogadás
            if not data:
                continue
            conn.sendall(b'Hello!')     # küldés
```

---

## 4. TCP kliens

```python
import socket

SERVER_ADDR = ('localhost', 10000)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(SERVER_ADDR)
    sock.sendall(b'Hello, Server!')     # küldés
    data = sock.recv(1024)              # fogadás
    print(data.decode())
```

---

## 5. UDP szerver

```python
import socket

SERVER_ADDR = ('localhost', 10000)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(SERVER_ADDR)
    sock.settimeout(1.0)   # opcionális timeout

    while True:
        try:
            data, client_addr = sock.recvfrom(1024)  # adat + feladó cím
            print(f'Kapott: {data.decode()} tőle: {client_addr}')
            sock.sendto(b'Hello!', client_addr)       # válasz küldése
        except socket.timeout:
            pass
```

---

## 6. UDP kliens

```python
import socket

SERVER_ADDR = ('localhost', 10000)

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.sendto(b'Hello, Server!', SERVER_ADDR)   # küldés célcímmel
    data, server_addr = sock.recvfrom(1024)        # fogadás
    print(data.decode())
```

> **Különbség TCP vs UDP:**
> - TCP: `connect()` + `sendall()` + `recv()`
> - UDP: `sendto(adat, cím)` + `recvfrom(bufmeret)` → `(adat, cím)`

---

## 7. TCP szerver – több kliens (select)

```python
import socket
import select

SERVER_ADDR = ('localhost', 10000)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.setblocking(False)   # NON-BLOCKING kötelező select-hez!
    server.bind(SERVER_ADDR)
    server.listen(5)

    inputs = [server]   # figyelt socketok listája

    while inputs:
        # select visszatér ha bármelyik socket olvasható
        # timeout=1: ne blokkoljunk örökké (KeyboardInterrupt miatt)
        readable, _, _ = select.select(inputs, [], [], 1)

        for sock in readable:
            if sock is server:
                # Új kliens
                conn, addr = server.accept()
                conn.setblocking(False)
                inputs.append(conn)
            else:
                # Meglévő klienstől adat
                data = sock.recv(1024)
                if not data:
                    # Kliens bontotta a kapcsolatot
                    inputs.remove(sock)
                    sock.close()
                else:
                    # Feldolgozás...
                    sock.sendall(b'OK')
```

> **select() hívás:**
> `readable, writable, exceptional = select.select(inputs, outputs, errors, timeout)`

---

## 8. Fájl beolvasás (TXT + JSON)

### TXT fájl (soronként: "szöveg szám")
```python
import random

with open('input.txt', 'r') as f:
    lines = f.readlines()       # ['almafa 4\n', 'kortefa 3\n', ...]

rand_idx = random.randint(1, 3)         # 1-3 közti szám
line = lines[rand_idx - 1].strip()      # 0-indexelt lista!
parts = line.split()
text, number = parts[0], int(parts[1])
```

### JSON fájl ({"1": ["szöveg", szám], ...})
```python
import json
import random

with open('input.json', 'r') as f:
    data = json.load(f)   # {"1": ["almafa", 4], ...}

rand_key = str(random.randint(1, 3))   # int-ből str kulcs!
entry = data[rand_key]
text, number = entry[0], entry[1]
```

---

## 9. Proxy minta (TCP → UDP)

```python
import socket, select, struct

tcp_packer = struct.Struct('4s i')
udp_packer = struct.Struct('5s i')
udp_resp   = struct.Struct('i')

CMD_MAP = {'IN': b'PUSH ', 'INCR': b'PLUS ', 'DECR': b'MINUS'}

def forward_to_udp(cmd, value, udp_addr):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
        udp.settimeout(2.0)
        udp.sendto(udp_packer.pack(CMD_MAP[cmd], value), udp_addr)
        data, _ = udp.recvfrom(udp_resp.size)
        (result,) = udp_resp.unpack(data)
        return result

# TCP szerver (select-tel) + parancs fogadásnál forward_to_udp() hívás
```

---

## 10. UDP fájlátvitel

```python
# KÜLDŐ (kliens)
BUFFER = 200
END = b'\x00'
with socket.socket(AF_INET, SOCK_DGRAM) as s, open('file.bin', 'rb') as f:
    s.settimeout(1.0)
    data = f.read(BUFFER)
    while data:
        try:
            s.sendto(data, SERVER_ADDR)
            reply, _ = s.recvfrom(BUFFER)   # ACK
            data = f.read(BUFFER)
        except socket.timeout:
            pass   # újraküldés (lehetne retry logika)
    s.sendto(END, SERVER_ADDR)   # vége jelzés

# FOGADÓ (szerver)
with socket.socket(AF_INET, SOCK_DGRAM) as s, open('out.bin', 'wb') as f:
    s.bind(SERVER_ADDR)
    s.settimeout(1.0)
    while True:
        try:
            data, addr = s.recvfrom(BUFFER)
            if data == END:
                break
            f.write(data)
            s.sendto(b'OK', addr)
        except socket.timeout:
            pass
```

---

## 11. Tipikus hibák és javításuk

| Hiba | Ok | Javítás |
|------|----|---------|
| `ConnectionRefusedError` | Szerver nem fut / rossz port | Indítsd el a szervert először |
| `OSError: [Errno 98] Address already in use` | Port foglalt | `setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)` |
| Null-bájtok a stringben | `struct` 20s kitölti nullákkal | `.strip('\x00')` vagy `.rstrip(b'\x00')` |
| `struct.error: unpack requires buffer of X bytes` | Hibás méret | `recv(packer.size)` – pontosan a struct méretét olvasd! |
| UDP nem kap választ | Timeout | `sock.settimeout(2.0)` |
| `setblocking(False)` után `BlockingIOError` | select nélkül nem-blokkoló hívás | Csak select-tel együtt használd |

---

## 12. Struct formátumok referencia (mintaZH)

| Feladat | Formátum | Leírás |
|---------|----------|--------|
| 1. feladat kliens küld | `'20s i'` | szöveg (20 bájt) + szám |
| 2. feladat kliens küld | `'4s i'` | parancs (IN/INCR/DECR) + érték |
| 3a. feladat UDP küld | `'5s i'` | parancs (PUSH/PLUS/MINUS) + érték |
| 3a. feladat UDP válasz | `'i'` | tárolt érték (struct, nem string!) |
| 5. skeleton serverUDP | `'15s i'` | hostname + port |
| 6. skeleton udp_calc | `'i i c'` | operandus1, operandus2, operator |
| 6. skeleton udp_calc válasz | `'f'` | float eredmény |

---

## Gyors sablon – TCP kliens struct-tal

```python
import socket, struct, random

packer = struct.Struct('20s i')
SERVER_ADDR = ('localhost', 10000)

text = input('Szöveg: ')
num  = random.randint(1, 10)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(SERVER_ADDR)
    s.sendall(packer.pack(text.encode(), num))
    raw = s.recv(1024)
    print(raw.decode().strip('\x00'))
```

## Gyors sablon – TCP szerver select()-tel

```python
import socket, select, struct

packer = struct.Struct('4s i')
SERVER_ADDR = ('localhost', 10000)
stored = 0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.setblocking(False)
    srv.bind(SERVER_ADDR)
    srv.listen(5)
    inputs = [srv]
    while inputs:
        r, _, _ = select.select(inputs, [], [], 1)
        for s in r:
            if s is srv:
                c, _ = srv.accept(); c.setblocking(False); inputs.append(c)
            else:
                d = s.recv(packer.size)
                if not d: inputs.remove(s); s.close()
                else:
                    cmd, val = packer.unpack(d)
                    cmd = cmd.decode().strip()
                    # ... feldolgozás ...
                    s.sendall(str(stored).encode())
```

## Gyors sablon – UDP szerver

```python
import socket, struct

packer = struct.Struct('5s i')
resp   = struct.Struct('i')
stored = 0

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('localhost', 10001))
    s.settimeout(1.0)
    while True:
        try:
            data, addr = s.recvfrom(packer.size)
            cmd, val = packer.unpack(data)
            cmd = cmd.decode().strip()
            # ... feldolgozás ...
            s.sendto(resp.pack(stored), addr)
        except socket.timeout: pass
```
