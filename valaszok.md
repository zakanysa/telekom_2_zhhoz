# Telekommunikacios halozatok - ZH kerdesek es valaszok

---

## 1. Mit jelent az AF_INET parameter?

Az **AF_INET** (Address Family - Internet) azt jelenti, hogy **IPv4 halozati kommunikaciot** hasznalunk. Ez a cimcsalad (address family) parameter a `socket()` fuggvenyben hatarozza meg, hogy a socket IPv4-es IP cimekkel fog dolgozni. Letezik meg **AF_INET6** is, ami IPv6-ot jelent.

---

## 2. Mikor kell a recv() fuggvenyt alkalmazni?

A `recv()` fuggvenyt **TCP (kapcsolat-orientalt) kommunikacioban** hasznaljuk **adatok fogadasara** egy mar letrejott kapcsolaton keresztul. Miutan a `connect()` (kliens oldalon) vagy `accept()` (szerver oldalon) letrehozta a kapcsolatot, a `recv()` fuggvennyel olvassuk be a masik fel altal kuldott adatokat. Parametere a maximalis fogadhato byte-ok szama (pl. `recv(1024)`).

---

## 3. Mit csinal a socket() fuggveny?

A `socket()` fuggveny **letrehoz egy uj socketet** (kommunikacios vegpontot). Parameterek:
- **Cimcsalad** (pl. `AF_INET` = IPv4)
- **Socket tipus** (pl. `SOCK_STREAM` = TCP, `SOCK_DGRAM` = UDP)

Pelda: `sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)` - ez letrehoz egy TCP socketet IPv4-gyel.

A fuggveny **meg nem csatlakozik sehova es nem bind-ol** - csak letrehozza a kommunikacios vegpontot.

---

## 4. Mi a kulonbseg a SOCK_STREAM es SOCK_DGRAM kozott?

| Jellemzo | SOCK_STREAM (TCP) | SOCK_DGRAM (UDP) |
|---|---|---|
| Protokoll | TCP | UDP |
| Kapcsolat | Kapcsolat-orientalt (connect kell) | Kapcsolat nelkuli |
| Megbizhatosag | Megbizhato, sorrendhelyes | Nem megbizhato, csomagvesztes lehetseges |
| Adatfolyam | Folytonos byte-stream | Onallo datagramok (uzenetek) |
| Sebesseg | Lassabb (overhead) | Gyorsabb |
| Hasznalat | Fajlatvitel, web, email | Video streaming, DNS, jatek |

---

## 5. Mit jelent a bind() muvelet?

A `bind()` **hozzarendel egy IP cimet es port szamot a sockethez**. Ezaltal megmondjuk az operacios rendszernek, hogy ez a socket melyik halozati interfeszen es melyik porton figyeljen. Jellemzoen a **szerver oldalon** hasznaljuk.

Pelda: `sock.bind(('localhost', 10000))` - a socket a localhost 10000-es portjahoz kototodik.

Ha nem bind-olunk, akkor az OS automatikusan valaszt egy cimet es portot (ez a kliens oldalon altalanos).

---

## 6. Mire szolgal a listen() fuggveny?

A `listen()` fuggveny **TCP szerveren** allitja a socketet **figyelo (listening) modba**, azaz jelzi az OS-nek, hogy a szerver kesz bejovo kapcsolatokat fogadni. A parametere a **backlog** erteke, ami megadja, hany bejovo kapcsolat varakozhat a sorban, mielott a szerver elutasitja oket.

Pelda: `sock.listen(1)` - maximum 1 kapcsolat varakozhat a sorban.

**Fontos:** Csak TCP-nel (SOCK_STREAM) hasznaljuk, UDP-nel **NEM kell** listen()!

---

## 7. Mit csinal az accept() fuggveny?

Az `accept()` fuggveny **elfogad egy bejovo kliens kapcsolatot** a figyelő TCP szerveren. Ez egy **blokkolobb muvelet** - varakozik, amig egy kliens csatlakozik.

Visszateresi ertekei:
- **connection (conn)**: egy uj socket objektum, ami a klienssel valo kommunikaciot biztositja
- **client_address**: a kliens IP cime es portja (tuple)

Pelda: `conn, addr = sock.accept()`

Ezutan a `conn` socketen keresztul kommunikalunk a klienssel, mig az eredeti szerver socket tovabb figyel.

---

## 8. Mikor hasznaljuk a connect() fuggvenyt?

A `connect()` fuggvenyt a **kliens oldalon** hasznaljuk, hogy **kapcsolodjon a szerverhez**. Megadjuk a szerver IP cimet es port szamat.

Pelda: `sock.connect(('localhost', 10000))`

- **TCP eseten**: letrehoz egy teljes kapcsolatot a szerverrel (haromlepeses kezfogassal / three-way handshake)
- **UDP eseten**: opcionalis, ha hasznaljuk, beallitja az alapertelmezett celcimet, igy utana `send()` es `recv()` hasznalhato `sendto()` es `recvfrom()` helyett

---

## 9. Mi a sendall() fuggveny elonye a send()-del szemben?

A `send()` fuggveny **nem garantalja**, hogy az osszes adatot elkuldi egyetlen hivással - visszaadja a tenylegesen elkuldott byte-ok szamat, ami kevesebb lehet, mint amit kuldeni akartunk.

A `sendall()` **garantalja, hogy az osszes adatot elkuldi**: automatikusan ismetli a kuldest, amig az osszes byte el nem ment. Ha hiba tortenik, kivetelt dob.

**Elony: Nem kell manuálisan kezelni a reszleges kuldeseket.** Tehat `sendall()` egyszerubb es biztonsagosabb.

---

## 10. Mit jelent a socket timeout?

A **socket timeout** az az **idokorlat** (masodpercekben), ameddig egy socket muvelet (pl. `recv()`, `accept()`, `connect()`) varakozik. Ha ez az ido letelik anelkul, hogy a muvelet befejezodne, egy `socket.timeout` **kivétel** dobodik.

- **Alapertelmezetten**: nincs timeout (vegtelen varakozas, azaz blokkol)
- **Timeout beallitva**: ha az ido letelik, `socket.timeout` kivetelt kapunk
- **0 ertek**: nem-blokkolo mod (azonnal visszater vagy hibat dob)

---

## 11. Mire valo a settimeout() fuggveny?

A `settimeout()` fuggveny **beallitja a socket timeout erteket masodpercekben**.

Pelda: `sock.settimeout(5.0)` - 5 masodperces timeout

Ertekek:
- **Pozitiv szam** (pl. 5.0): ennyi masodpercet var, utana `socket.timeout` kivetelt dob
- **None**: vegtelen varakozas (blokkolo mod, ez az alapertelmezett)
- **0**: nem-blokkolo mod

Hasznalata fontos **UDP-nel**, ahol nincs garancia az adatok megerkezesere, igy megakadalyozhatjuk, hogy a program orokre varakozzon.

---

## 12. Mi tortenik, ha a recv() 0 byte-ot ad vissza?

Ha a `recv()` **ures byte-stringet** (`b''`) ad vissza, az azt jelenti, hogy a **masik fel lezarta a kapcsolatot** (a masik fel meghivta a `close()` fuggvenyt). Ez a TCP kapcsolat lezarasanak normalis jelzese.

Ilyenkor nekunk is le kell zarni a socketet a `close()` hivással. Ez **nem hibajelzes**, hanem a normalis kapcsolatbontasi mechanizmus resze.

---

## 13. Mit csinal a close() fuggveny?

A `close()` fuggveny **lezarja a socketet**, felszabaditva az operacios rendszer altal hozzarendelt eroforrasokat. Lezaras utan a socket tobbe nem hasznalhato.

- TCP eseten a `close()` elküldi a kapcsolatbontási jelzést a masik felnek
- A masik fel `recv()` hívása ilyenkor `b''`-t (0 byte-ot) ad vissza
- Fontos, hogy mindig zarjuk le a socketet, kulonben eroforras-szivargás (resource leak) lephet fel

Eleg gyakran `with` statementtel hasznaljak, ami automatikusan lezarja.

---

## 14. Mi a localhost jelentese?

A **localhost** a **sajat szamitogep halozati cime**. Az IP cime **127.0.0.1** (IPv4) vagy **::1** (IPv6). Erre a cimre kuldott csomagok **nem hagyják el a gepcsomagot** - a sajat gepen belul kommunikalunk vele (loopback interface).

Fejlesztes es teszteles soran hasznaljuk, amikor a szerver es a kliens ugyanazon a gepen fut.

---

## 15. Mit jelent a port szam?

A **port szam** egy **16 bites egesz szam (0-65535)**, ami egy adott alkalmazast vagy szolgaltatast azonosit egy halozati gepen. Mig az IP cim a gepet azonositja, a port szam megmondja, hogy a gepen belul **melyik programnak** szol az adat.

- **0-1023**: jol ismert portok (well-known ports) - pl. 80 = HTTP, 443 = HTTPS, 22 = SSH
- **1024-49151**: regisztralt portok
- **49152-65535**: dinamikus/privat portok

Egy alkalmazas a `bind()` fuggvennyel foglal le egy portot.

---

## 16. Mi az IP cim szerepe?

Az **IP cim** (Internet Protocol cim) a halozatban levo **eszkozok egyedi azonositoja**. Szerepe, hogy **egyertelmuen azonositsa a kuldo es fogado gepcsomagot** a halozatban, igy a csomagok a megfelelo celallomaskoz jussanak el.

- **IPv4**: 32 bites (pl. 192.168.1.1)
- **IPv6**: 128 bites (pl. fe80::1)

A socket programozasban az IP cim es a port szam egyutt alkot egy egyedi vegpontot (endpoint).

---

## 17. Mi a kliens-szerver architektura?

A **kliens-szerver** modell egy halozati kommunikacios architektura:

- **Szerver**: egy program, ami **var a bejovo kapcsolatokra**, kiszolgalja a kereseket. Altalaban folyamatosan fut, bind()-ol egy cimre es portra, es listen()-nel figyel.
- **Kliens**: egy program, ami **kezdemenyezi a kapcsolatot** a szerverrel (`connect()`), kerest kuld es valaszt var.

Jellemzok:
- A szerver eloszor indul el es var
- A kliens csatlakozik a szerverhez
- Egy szerver tobb klienst is kiszolgalhat
- A szerepek asszimmetrikusak: a szerver szolgaltat, a kliens kerest kuld

---

## 18. Mit jelent a "blocking" socket muvelet?

A **blokkolo (blocking)** socket muvelet azt jelenti, hogy a program **megall es varakozik**, amig a muvelet befejezodik. Az adott szal (thread) nem halad tovabb, amig az eredmeny meg nem erkezik.

Pelda blokkolo muveletek:
- `accept()` - var, amig egy kliens csatlakozik
- `recv()` - var, amig adat erkezik
- `connect()` - var, amig a kapcsolat letrejon

Ez az **alapertelmezett** viselkedes. A `settimeout()` segitsegevel korlatozhato a varakozasi ido, vagy a timeout 0-ra allitasaval nem-blokkolo modba kapcsolhato.

---

## 19. Hogyan hozunk letre TCP socketet?

```python
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

- `socket.AF_INET` - IPv4 cimcsalad
- `socket.SOCK_STREAM` - TCP protokoll (megbizhato, kapcsolat-orientalt byte-stream)

Ez letrehozza a socketet, de meg nem csatlakozik sehova. Ezutan kell bind/listen/accept (szerver) vagy connect (kliens).

---

## 20. Mi a TCP szerver helyes sorrendje?

1. **`socket()`** - socket letrehozasa
2. **`bind()`** - cim es port hozzarendelese
3. **`listen()`** - figyelomodba allitas
4. **`accept()`** - bejovo kapcsolat elfogadasa (visszaad egy uj socketet)
5. **`recv()` / `sendall()`** - adatkommunikacio az uj socketen
6. **`close()`** - kliens socket, majd szerver socket lezarasa

Pelda:
```python
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 10000))
server.listen(1)
conn, addr = server.accept()
data = conn.recv(1024)
conn.sendall(b'valasz')
conn.close()
server.close()
```

---

## 21. Mi a TCP kliens helyes sorrendje?

1. **`socket()`** - socket letrehozasa
2. **`connect()`** - csatlakozas a szerverhez (IP + port)
3. **`sendall()` / `recv()`** - adatkommunikacio
4. **`close()`** - socket lezarasa

Pelda:
```python
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 10000))
client.sendall(b'uzenet')
data = client.recv(1024)
client.close()
```

---

## 22. Mit jelent a SO_REUSEADDR opcio?

A **SO_REUSEADDR** egy socket opcio, amely lehetove teszi, hogy **ujra lehessen hasznalni egy cimet es portot**, amelyet nemreg zartak le. Normalis esetben, ha egy socketet lezarunk, az operacios rendszer meg egy ideig (TIME_WAIT allapot, ~1-4 perc) lefoglalja azt a portot. A SO_REUSEADDR opcio **atlepi ezt a varakozast**, igy azonnal ujra bind-olhatunk ugyanarra a portra.

Ez kulonosen hasznos **fejlesztes soran**, amikor gyakran ujrainditjuk a szervert, es nem akarjuk megvarni, amig a port felszabadul.

---

## 23. Hogyan allitjuk be a SO_REUSEADDR opciot?

```python
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
```

- `socket.SOL_SOCKET` - socket szintu opcio
- `socket.SO_REUSEADDR` - az opcio neve
- `1` - bekapcsolas (True)

Ezt a `bind()` **elott** kell meghivni!

---

## 24. Mi tortenik, ha a listen() parametere 1?

A `listen(1)` azt jelenti, hogy a szerver **maximum 1 varakozo kapcsolatot** enged a sorban (backlog). Ha mar van 1 feldolgozatlan kapcsolat a sorban es ujabb kliens probal csatlakozni, az **elutasitasra kerul** (connection refused).

Ez nem azt jelenti, hogy a szerver osszesen csak 1 klienst tud kiszolgalni - hanem hogy **egyszerre csak 1 varakozhat** az accept() hivasig. Miutan az accept() elfogadta a kapcsolatot, ujra lesz hely a sorban.

---

## 25. Hogyan kuldunk binaris adatokat TCP-n?

Binaris adatokat a **`struct` modul** segitsegevel csomagolunk be es kuldunk:

```python
import struct

# Becsomagolas (pack)
data = struct.pack('I f', 42, 3.14)  # egesz szam + lebegopontos szam
sock.sendall(data)

# Kicsomagolas (unpack) a fogado oldalon
data = sock.recv(1024)
num, flt = struct.unpack('I f', data)
```

A `struct.pack()` Python ertekeket binaris formátumra alakit, a `struct.unpack()` pedig visszaalakitja oket.

---

## 26. Mi a struct modul szerepe socket programozasban?

A **struct modul** Python ertekeket (szamok, stringek) **binaris formátumba** alakit es vissza. Ez azert fontos, mert a halozaton **byte-ok** utaznak, nem Python objektumok.

Fo fuggvenyek:
- **`struct.pack(format, values...)`** - Python ertekekbol binaris adat
- **`struct.unpack(format, data)`** - binaris adatbol Python ertekek (tuple-t ad vissza)

Formatumkodok:
- `I` = unsigned int (4 byte)
- `i` = signed int (4 byte)
- `f` = float (4 byte)
- `d` = double (8 byte)
- `1s` = 1 byte-os string
- `10s` = 10 byte-os string

---

## 27. Hogyan kezeljuk a tobbszoros kliens kapcsolatokat?

Tobbfele megoldas letezik:

**1. Szekvencialis (egyszerre egy kliens):**
```python
while True:
    conn, addr = server.accept()
    # kiszolgalas
    conn.close()
```

**2. select() hasznalata (I/O multiplexing):**
```python
import select
readable, _, _ = select.select(input_sockets, [], [], timeout)
```
A `select()` figyeli tobb socket allapotat egyszerre, es megmondja, melyiken van olvasni valo adat.

**3. Threading (szalakkal):**
Minden kliensnek kulon szal (thread).

A ZH-ban a **select()** alapu megoldas a legfontosabb.

---

## 28. Mi a with statement elonye socket programozasban?

A `with` statement biztositja, hogy a socket **automatikusan lezarodjon**, meg akkor is, ha hiba (kivetel) tortenik. Ez megakadalyozza az eroforras-szivargas (resource leak) problemat.

```python
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(('localhost', 10000))
    sock.sendall(b'hello')
    data = sock.recv(1024)
# itt mar automatikusan lezarodott a socket
```

A `with` nelkul a `try/finally` blokkban kellene manuálisan lezarni a socketet.

---

## 29. Hogyan olvassunk es kuldjunk fajlt TCP-n hatekonyan?

**Kuldes:**
```python
with open('file.bin', 'rb') as f:
    while True:
        chunk = f.read(1024)   # darabonkent olvassuk
        if not chunk:
            break
        sock.sendall(chunk)    # sendall() garantalja a teljes kuldest
```

**Fogadas:**
```python
with open('received.bin', 'wb') as f:
    while True:
        data = sock.recv(1024)
        if not data:           # ha 0 byte, a kapcsolat lezarult
            break
        f.write(data)
```

**Kulcs pontok:**
- Darabokban (chunk) olvassuk/kuldjuk, nem egyben (memoriahatekony)
- `sendall()` garantalja a teljes kuldest
- `recv()` ures valasza (`b''`) jelzi a kapcsolat veget

---

## 30. Mit csinal a struct.pack()?

A `struct.pack()` **Python ertekeket binaris byte-okka alakit** a megadott formatum szerint.

```python
import struct
data = struct.pack('I f 1s', 42, 3.14, b'A')
```

- Elso parameter: **formatum string** (milyen tipusu adatokat csomagolunk)
- Tobbi parameter: az **ertekek** a formatum szerint
- Visszateresi ertek: **bytes** objektum

Ez szukseges, mert a halozaton nyers byte-okat kuldunk, nem Python objektumokat.

---

## 31. Mit csinal a struct.unpack()?

A `struct.unpack()` **binaris byte-okat Python ertekekke alakit** vissza a megadott formatum szerint.

```python
import struct
values = struct.unpack('I f 1s', data)
# values egy tuple, pl. (42, 3.14, b'A')
```

- Elso parameter: **formatum string** (ugyanaz, mint a pack-nel hasznalt)
- Masodik parameter: a **binaris adat** (bytes)
- Visszateresi ertek: **tuple** a kicsomagolt ertekekkel

**Fontos:** A formatum stringnek pontosan meg kell egyeznie azzal, amivel az adatot becsomagoltak!

---

## 32. Mi a 'f f 1s' formatum jelentese struct-ban?

- **`f`** = float (egypontos lebegopontos szam, 4 byte)
- **`f`** = float (meg egy float, 4 byte)
- **`1s`** = 1 byte hosszu string (bytes)

Tehat az **`'f f 1s'`** formatum osszesen **9 byte-os** adatot jelent: ket darab float es egy 1 byte-os string.

Pelda:
```python
data = struct.pack('f f 1s', 1.5, 2.7, b'X')
a, b, c = struct.unpack('f f 1s', data)
# a = 1.5, b = 2.7, c = b'X'
```

---

## 33. Hogyan kezeljuk a reszleges adatkuldest TCP-ben?

TCP-ben a `send()` nem feltetlenul kuldi el az osszes adatot egyszerre. Ket megoldas:

**1. sendall() hasznalata (egyszerubb):**
```python
sock.sendall(data)  # automatikusan elkuldi az osszeset
```

**2. Manualis kezeles send()-del:**
```python
total_sent = 0
while total_sent < len(data):
    sent = sock.send(data[total_sent:])
    if sent == 0:
        raise RuntimeError("Kapcsolat megszakadt")
    total_sent += sent
```

A **`sendall()` az ajanlott megoldas**, mert automatikusan megoldja a reszleges kuldest.

---

## 34. Mi tortenik accept() utan TCP szerveren?

Az `accept()` **ket dolgot ad vissza**:
1. **Uj socket** (`conn`): ezen keresztul kommunikalunk az adott klienssel
2. **Kliens cime** (`addr`): a kliens IP cime es portja (tuple)

```python
conn, addr = server.accept()
```

Az eredeti szerver socket (`server`) **tovabbra is figyel** uj kapcsolatokra. A kommunikacio a klienssel a **`conn` socketen** keresztul tortenik (recv, sendall). Vegul a `conn.close()` zarjuk le a kliens kapcsolatot.

**Fontos:** Ket kulon socket van - a szerver socket (figyelesre) es a kliens socket (kommunikaciora).

---

## 35. Hogyan zarjuk be helyesen a kliens kapcsolatot a TCP szerveren?

```python
conn, addr = server.accept()
try:
    # kommunikacio
    data = conn.recv(1024)
    conn.sendall(b'valasz')
finally:
    conn.close()  # kliens socket lezarasa
```

Vagy `with` statement-tel:
```python
conn, addr = server.accept()
with conn:
    data = conn.recv(1024)
    conn.sendall(b'valasz')
# automatikusan lezarodik
```

**Fontos:** Csak a kliens socketet (`conn`) zarjuk le, a szerver socketet (`server`) csak akkor, ha a szerver le akar allni.

---

## 36. Mi a kulonbseg a server socket es client socket kozott TCP-ben?

| Jellemzo | Server socket | Client socket (conn) |
|---|---|---|
| Letrehozas | `socket()` hivassal | `accept()` adja vissza |
| Szerepe | Bejovo kapcsolatok figyelese | Egy adott klienssel kommunikacio |
| Muveletek | `bind()`, `listen()`, `accept()` | `recv()`, `sendall()`, `close()` |
| Eletciklus | A szerver elete soran aktiv | Egy kliens kapcsolat idejeig el |
| Darabszam | 1 db a szerveren | Annyi, ahany kliens csatlakozott |

A server socket **nem kuld es nem fogad adatot** kozvetlenul - csak uj kapcsolatokat fogad el. Az adat a client socketen (conn) megy.

---

## 37. Hogyan mukodik a fajlkuldes TCP-vel?

**Kuldo oldal (kliens vagy szerver):**
1. Fajl megnyitasa binaris modban (`'rb'`)
2. Fajl olvasasa darabokban (chunk)
3. Minden darab kuldese `sendall()` segitsegevel
4. Kuldes vegen socket lezarasa (jelzes a fogadonak)

**Fogado oldal:**
1. Fajl megnyitasa irasra binaris modban (`'wb'`)
2. `recv()` ciklusban amig `b''`-t nem kapunk
3. Minden fogadott darab irasa a fajlba

**A fogadó onnan tudja, hogy vege az atvitelnek, hogy a `recv()` ures byte-stringet (`b''`) ad vissza**, ami azt jelenti, a kuldo lezarta a kapcsolatot.

---

## 38. Mit jelent a ('localhost', 10000) par?

Ez egy **socket cim tuple**, ami ket reszbol all:
- **`'localhost'`** - a celgep cime (127.0.0.1, a sajat gep)
- **`10000`** - a port szam

Ez a par egyutt egyertelmuen azonosit egy **halozati vegpontot**. Hasznalhato a `bind()`, `connect()` es `sendto()` fuggvenyekben.

Pelda: `sock.bind(('localhost', 10000))` - a socket a sajat gep 10000-es portjahoz kotodik.

---

## 39. Hogyan hozunk letre UDP socketet?

```python
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
```

- `socket.AF_INET` - IPv4
- `socket.SOCK_DGRAM` - UDP protokoll (datagram-alapu, kapcsolat nelkuli)

A TCP-vel ellentetben **nem kell `connect()`, `listen()` vagy `accept()`** (bar a connect() opcionalis).

---

## 40. Mi a fo kulonbseg UDP es TCP kozott?

| Jellemzo | TCP (SOCK_STREAM) | UDP (SOCK_DGRAM) |
|---|---|---|
| Kapcsolat | Kapcsolat-orientalt | Kapcsolat nelkuli |
| Megbizhatosag | Megbizhato (ujrakuldes, sorrendiseg) | Nem megbizhato (csomagvesztes lehetseges) |
| Sorrend | Garantalt | Nem garantalt |
| Sebesség | Lassabb | Gyorsabb |
| Adategyseg | Byte-stream | Datagram (kulonallo csomagok) |
| listen()/accept() | Kell | Nem kell |
| Kuldes/fogadas | send()/recv() | sendto()/recvfrom() |
| Hasznalat | Fajlatvitel, web, email | DNS, streaming, jatekok |

---

## 41. Mit csinal a sendto() fuggveny?

A `sendto()` **UDP datagramot kuld** egy megadott celcimre. Mivel UDP kapcsolat nelkuli, minden egyes kuldesnel meg kell adni a celcimet.

```python
sock.sendto(data, ('localhost', 10000))
```

Parameterek:
- **data**: a kuldendo adat (bytes)
- **address**: a cel cim es port (tuple)

Visszateresi ertek: az elkuldott byte-ok szama.

TCP-ben nincs szukseg `sendto()`-ra, mert ott a `connect()` mar meghatározta a celcimet.

---

## 42. Mit ad vissza a recvfrom() fuggveny?

A `recvfrom()` **UDP adatot fogad** es visszaadja **ket erteket**:

```python
data, address = sock.recvfrom(4096)
```

- **data** (bytes): a fogadott adat
- **address** (tuple): a kuldo IP cime es portja, pl. `('127.0.0.1', 54321)`

A `4096` parameter a maximalis fogadhato byte-ok szama.

Ez azert fontos UDP-nel, mert mivel nincs allo kapcsolat, **minden csomagnal tudnunk kell, ki kuldte**, hogy valaszolni tudjunk.

---

## 43. Kell-e connect() UDP kliensnél?

**Nem kötelezo**, de hasznalhato. UDP kliens ket modon mukodhet:

**connect() nelkul (tipikus):**
```python
sock.sendto(data, ('localhost', 10000))
data, addr = sock.recvfrom(4096)
```

**connect()-tel:**
```python
sock.connect(('localhost', 10000))
sock.send(data)        # nem kell cimet megadni
data = sock.recv(4096)  # nem kell cimet visszakapni
```

A `connect()` UDP-nel **nem hoz letre valodi kapcsolatot**, csak beallitja az alapertelmezett celcimet, igy egyszerubben hasznalhato a `send()` es `recv()`.

---

## 44. Kell-e listen() UDP szervernal?

**NEM!** A `listen()` **kizarolag TCP-hez** valo. UDP-nel nincs szukseg ra, mert UDP kapcsolat nelkuli protokoll - nincs "figyeles" vagy "kapcsolat elfogadas".

UDP szerveren a sorrend:
1. `socket()` - socket letrehozas
2. `bind()` - cim/port hozzarendeles
3. `recvfrom()` - adatfogadas (a kuldo cimet is megkapjuk)

Nincs `listen()` es nincs `accept()` sem!

---

## 45. Mi az UDP szerver alapveto sorrendje?

1. **`socket()`** - UDP socket letrehozasa (`SOCK_DGRAM`)
2. **`bind()`** - cim es port hozzarendelese
3. **`recvfrom()`** - adat fogadasa (megkapjuk a kuldo cimet is)
4. **`sendto()`** - valasz kuldese a kuldo cimere
5. **`close()`** - socket lezarasa

```python
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('localhost', 10000))
data, addr = sock.recvfrom(4096)
sock.sendto(b'valasz', addr)
sock.close()
```

**Nincs listen(), nincs accept()!**

---

## 46. Mi az UDP kliens alapveto sorrendje?

1. **`socket()`** - UDP socket letrehozasa (`SOCK_DGRAM`)
2. **`sendto()`** - adat kuldese a szerver cimere
3. **`recvfrom()`** - valasz fogadasa
4. **`close()`** - socket lezarasa

```python
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(b'uzenet', ('localhost', 10000))
data, addr = sock.recvfrom(4096)
sock.close()
```

**Nem kell `bind()`, nem kell `connect()`!** (Az OS automatikusan kioszt egy portot.)

---

## 47. Mit ad vissza a recvfrom() pontosan?

A `recvfrom()` egy **tuple-t** ad vissza ket elemmel:

```python
data, address = sock.recvfrom(buffer_size)
```

1. **`data`** (bytes): a fogadott adat byte-okban
2. **`address`** (tuple): `(ip_cim, port_szam)` - a kuldo cime

Pelda:
```python
data, addr = sock.recvfrom(4096)
# data = b'Hello'
# addr = ('127.0.0.1', 54321)
```

A `buffer_size` (pl. 4096) a **maximalis fogadhato byte-ok szama** egyetlen hivassal.

---

## 48. Milyen parametereket var a sendto()?

A `sendto()` **ket parametert** var:

```python
sock.sendto(data, address)
```

1. **`data`** (bytes): a kuldendo adat binaris formaban
2. **`address`** (tuple): a cel cim `(ip_cim, port_szam)` formaban

Pelda:
```python
sock.sendto(b'Hello UDP', ('localhost', 10000))
```

Visszateresi ertek: az elkuldott byte-ok szama (int).

---

## 49. Mi a UDP datagram elmeleti maximalis merete?

Az **UDP datagram elmeleti maximalis merete 65535 byte** (65507 byte hasznos adat + 8 byte UDP fejlec + 20 byte IP fejlec). Ez a 16 bites hossz mezobol adodik az UDP fejlecben.

**Gyakorlatban** azonban:
- A halozati MTU (Maximum Transmission Unit) jellemzoen **1500 byte** (Ethernet)
- Ennel nagyobb datagramok **fragmentalodasnak**, ami csomagvesztest okozhat
- Ajanlott meretnél maradni **512-8192 byte** kozott
- A `recvfrom()` buffermeretet ennek megfeleloen kell beallitani

---

## 50. Mi tortenik, ha UDP csomag elveszik?

**Semmi!** Az UDP **nem garantalja a csomagok kézbesítését**. Ha egy UDP datagram elvesz a halozatban:

- **Nincs automatikus ujrakuldes** (TCP-vel ellentetben)
- **Nincs ertesites** a kuldőnek
- **Nincs hibajelzes** - a fogado oldal egyszeruen nem kap adatot
- A `recvfrom()` **orokre varakozik** (ha nincs timeout beallitva)

Ezert fontos UDP-nel **timeout-ot beallitani** (`settimeout()`), hogy ne varakozzon a program vegtelen ideig, es szukség eseten megoldhassuk az ujraküldest alkalmazas szinten.

---

## 51. Mi a timeout szerepe UDP-nel?

A timeout **letfontossagu UDP-nel**, mert:

1. UDP nem megbizhato - csomagok elveszhetnek
2. `recvfrom()` blokkol (varakozik) alapertelmezetten
3. Ha a csomag elveszett, a program **orokre varakozna**

Megoldas:
```python
sock.settimeout(5.0)  # 5 masodperc timeout
try:
    data, addr = sock.recvfrom(4096)
except socket.timeout:
    print("Nem erkezett valasz - csomag elveszhetett")
```

A timeout lehetove teszi:
- Csomagvesztes detektalasa
- Ujrakuldes megvalositasa
- A program nem akad meg vegtelen varakozasban

---

## 52. Kell-e bind() az UDP kliensnek?

**Nem kell!** Az UDP kliensnek altalaban nem szükseges a `bind()` meghivasa. Az operacios rendszer **automatikusan kioszt egy veletlen (ephemeral) portot** az elso `sendto()` hivaskor.

**Mikor kell megis bind()?**
- Ha a kliens egy **fix porton** akar figyelni
- Ha a kliens **egyben szerver is** (mindket iranyu kommunikacio fix porton)

De a tipikus UDP kliens eseteben: `socket()` -> `sendto()` -> `recvfrom()` -> `close()`, bind() **nelkul**.

---

## 53. Mit jelent az "I I 1s" struct formatum?

- **`I`** = unsigned int (elojel nelkuli egesz szam, **4 byte**)
- **`I`** = meg egy unsigned int (**4 byte**)
- **`1s`** = 1 byte-os string (bytes, **1 byte**)

Osszesen: **9 byte** adat.

Pelda:
```python
data = struct.pack('I I 1s', 100, 200, b'A')
a, b, c = struct.unpack('I I 1s', data)
# a = 100, b = 200, c = b'A'
```

Fontos: `I` (nagybetu) = **unsigned** int (0-tol 4294967295-ig), `i` (kisbetu) = **signed** int (-2147483648-tol 2147483647-ig).

---

## 54. Hogyan kezeljuk a timeout kivetelt UDP-nel?

```python
sock.settimeout(5.0)

try:
    sock.sendto(data, server_address)
    response, addr = sock.recvfrom(4096)
    print(f"Valasz: {response}")
except socket.timeout:
    print("Timeout - nem erkezett valasz")
    # itt lehet ujraküldest megvalositani
```

A `socket.timeout` kivetel akkor dobodik, amikor a beallitott ido letelik anelkul, hogy adat erkezne. Ezt **try-except** blokkal kezeljuk.

Lehetseges reakciok timeout-ra:
- Ujrakuldes (retry)
- Hibauzenet
- Tovabblepés masik szerverre

---

## 55. Mi a fo kulonbseg TCP es UDP file kuldes kozott?

| Jellemzo | TCP fajlkuldes | UDP fajlkuldes |
|---|---|---|
| Megbizhatosag | Megbizhato, garantalt kezbesiotes | Csomagok elveszhetnek |
| Sorrend | Garantalt | Nem garantalt, osszekeveredhetnek |
| Kapcsolat | Kell (connect/accept) | Nem kell |
| Hibakezeles | Automatikus (TCP kezeli) | Nekunk kell megoldani |
| Vege jelzes | `recv()` -> `b''` (socket lezaras) | Kulon jelezni kell (pl. spec. csomag) |
| Egyszeruseg | Egyszerubb (stream) | Bonyolultabb (darabolás, sorszamozas kell) |
| Hasznalat | Nagy fajlok, megbizhato atvitel | Kis adatok, sebesseg fontosabb |

**TCP egyszerubb es megbizhatobb** fajlkuldesre. UDP-nel nekunk kell kezelni a csomagvesztest, sorrendet es nyugtazast.

---

## 56. Mi a proxy szerver szerepe?

A **proxy szerver** egy **kozvetito** a kliens es a celszerver kozott. A kliens a proxy-nak kuldi a kereset, a proxy tovabbitja a celszervernek, majd a valaszt visszakuldi a kliensnek.

Szerepei:
- **Kozvetites**: keres/valasz tovabbitasa
- **Szures**: meghatarozott URL-ek vagy tartalmak blokkolasa
- **Gyorsitotarazas (cache)**: gyakran kert tartalmak helyi tarolasa
- **Anonimitas**: a kliens IP cimenek elrejtese
- **Naplozas**: halozati forgalom monitorozasa

A proxy szerver **mind a kliens, mind a szerver szerepet betolti**: a kliens fele szerverkent, a celszerver fele klienskent viselkedik.

---

## 57. Mit csinal a select() fuggveny?

A `select()` fuggveny **I/O multiplexinget** valosit meg: **egyszerre figyel tobb socketet**, es megmondja, melyiken tortent esemeny (melyik kész olvasasra, irasra, vagy hol tortent hiba).

```python
import select
readable, writable, exceptional = select.select(rlist, wlist, xlist, timeout)
```

Parameterek:
- **rlist**: figyelendo socketek olvasasra
- **wlist**: figyelendo socketek irasra
- **xlist**: figyelendo socketek hibakra
- **timeout**: varakozasi ido (masodpercben, None = vegtelen)

Ez lehetove teszi, hogy **egyetlen szalban tobb klienst** szolgaljunk ki.

---

## 58. Mik a select() visszateresi ertekei?

A `select()` **harom listat** ad vissza:

```python
readable, writable, exceptional = select.select(rlist, wlist, xlist, timeout)
```

1. **readable**: socketek, amelyeken **van olvasni valo adat** (vagy uj kapcsolat erkezetett az accept()-hez)
2. **writable**: socketek, amelyekre **lehet irni** (van hely a kuldo pufferben)
3. **exceptional**: socketek, amelyeken **hiba tortent**

Ha a **timeout letelik** es semmi nem tortent, mindharom lista **ures** lesz.

Pelda:
```python
readable, _, _ = select.select([server_sock, client_sock], [], [], 1.0)
for sock in readable:
    if sock is server_sock:
        conn, addr = sock.accept()  # uj kapcsolat
    else:
        data = sock.recv(1024)      # adat erkezett
```

---

## 59. Hogyan szurhetjuk a HTTP kereseket proxy-ban?

A proxy szerver elemzi a bejovo HTTP kerest, es ellenőrzi, hogy az URL vagy a tartalom megengedett-e:

```python
# HTTP keres fogadasa
request = client_socket.recv(4096).decode()

# URL kinyerese a keresbol
# pl. "GET http://example.com/page HTTP/1.1"

# Tiltott oldalak listaja
blocked = ['blocked-site.com', 'bad-content.com']

if any(site in request for site in blocked):
    # Tiltott oldal - 403 Forbidden vagy 404 valasz
    client_socket.sendall(b'HTTP/1.1 404 Not Found\r\n\r\n')
else:
    # Engedelyezett - tovabbitás a celszervernek
    # ... proxy tovabbitasi logika
```

A szures tortenhet **URL**, **domain**, **kulcsszavak**, vagy **tartalom** alapjan.

---

## 60. Mit jelent a 404 HTTP statuszkod?

A **404 Not Found** azt jelenti, hogy a kert **eroforras (oldal, fajl) nem talalhato** a szerveren. A szerver elerheto, de a megadott URL-en nincs tartalom.

Proxy szerver kontextusaban a **404-et hasznalhatjuk blokkolt oldalak jelzesere** is: ha a proxy nem engedelyezi egy oldal elerest, 404 valaszt kuldhet a kliensnek.

Gyakori HTTP statuszkodok:
- **200 OK**: sikeres keres
- **301**: atiranyitas (moved permanently)
- **403 Forbidden**: hozzaferes megtagadva
- **404 Not Found**: nem talalhato
- **500 Internal Server Error**: szerverhiba

---

## 61. Mi tortenik, ha select() timeout-ol?

Ha a `select()` timeout erteke letelik es **egyetlen socketen sem tortent esemeny**, akkor **mindharom visszateresi lista ures** lesz:

```python
readable, writable, exceptional = select.select(inputs, [], [], 5.0)

if not readable:
    print("5 masodpercig semmi nem tortent")
else:
    for sock in readable:
        # feldolgozas...
```

Ha a timeout **None**: a `select()` vegtelen ideig var (blokkol), amig valamelyik socketen esemeny nem tortenik.

Ha a timeout **0**: azonnal visszater (nem-blokkolo mod), megmutatja az aktualis allapotot.

---

## 62. Mikor dobodik socket.timeout kivetel?

A `socket.timeout` kivetel akkor dobodik, amikor egy **socket muvelet nem fejezodik be a beallitott idon belul**:

- **`recv()` / `recvfrom()`**: nem erkezett adat a timeout idon belul
- **`accept()`**: nem csatlakozott kliens a timeout idon belul
- **`connect()`**: nem sikerult csatlakozni a timeout idon belul
- **`send()` / `sendall()`**: nem sikerult elkuldeni az adatot a timeout idon belul

A timeout-ot a `settimeout()` fuggvennyel allitjuk be:
```python
sock.settimeout(5.0)  # 5 masodperc
try:
    data = sock.recv(1024)
except socket.timeout:
    print("Timeout tortent!")
```

---

## 63. Hogyan detektaljuk a kapcsolat megszakadast TCP-ben?

A kapcsolat megszakadasat **tobbifelekeppen** detektalhatjuk:

**1. recv() ures valaszt ad:**
```python
data = conn.recv(1024)
if not data:  # b'' - ures bytes
    print("Kapcsolat lezarult")
    conn.close()
```
Ez a **normalis kapcsolatzaras** jelzese (a masik fel close()-t hivott).

**2. send() / recv() kivetelt dob:**
- `BrokenPipeError` - a masik fel mar bezarta a kapcsolatot
- `ConnectionResetError` - a kapcsolat varatlanul megszakadt
- `ConnectionRefusedError` - a cel elutasitotta a kapcsolatot

**3. Timeout:**
- Ha beallitottunk timeout-ot es letelik: `socket.timeout` kivetel

**A legfontosabb:** ha `recv()` visszater `b''`-vel, a **kapcsolat lezarult**.

---

## 64. Mi a leggyakoribb oka a bind() sikertelensegenek?

A leggyakoribb ok: **"Address already in use" (OSError: [Errno 98])** - a megadott port **mar foglalt**.

Okok:
1. **Masik program** mar használja azt a portot
2. **Elozo futtatásbol** meg TIME_WAIT allapotban van a port (nemreg zartuk le)
3. **Nincs jogosultsag** a porthoz (0-1023 portokhoz root/admin kell)

Megoldasok:
- **SO_REUSEADDR** beallitasa (a leggyakoribb megoldas):
```python
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('localhost', 10000))
```
- Masik port hasznalata
- Varas, amig a port felszabadul
- Az adott portot hasznaló program leallitasa

---

## OSSZEFOGLALO TABLA - Legfontosabb kulonbsegek

### TCP vs UDP muveletek

| Muvelet | TCP | UDP |
|---|---|---|
| Socket letrehozas | `SOCK_STREAM` | `SOCK_DGRAM` |
| Szerver bind | Kell | Kell |
| listen() | **Kell** | **Nem kell** |
| accept() | **Kell** | **Nem kell** |
| Kliens connect() | **Kell** | **Nem kell** (opcionalis) |
| Kuldes | `send()` / `sendall()` | `sendto()` |
| Fogadas | `recv()` | `recvfrom()` |
| Kapcsolat vege | `recv()` -> `b''` | Kulon jelezni kell |

### TCP szerver sorrend
`socket()` -> `bind()` -> `listen()` -> `accept()` -> `recv()`/`sendall()` -> `close()`

### TCP kliens sorrend
`socket()` -> `connect()` -> `sendall()`/`recv()` -> `close()`

### UDP szerver sorrend
`socket()` -> `bind()` -> `recvfrom()` -> `sendto()` -> `close()`

### UDP kliens sorrend
`socket()` -> `sendto()` -> `recvfrom()` -> `close()`

### struct formatumkodok
| Kod | Tipus | Meret |
|---|---|---|
| `I` | unsigned int | 4 byte |
| `i` | signed int | 4 byte |
| `f` | float | 4 byte |
| `d` | double | 8 byte |
| `1s` | 1 byte string | 1 byte |

### Fontos port/cim tudnivalok
- **localhost** = 127.0.0.1 (sajat gep)
- **Port tartomany**: 0-65535
- **Well-known portok**: 0-1023
- **SO_REUSEADDR**: bind() elott kell beallitani, megoldja az "Address already in use" problemat
