# beadando1
# Projekt cím: Tetoválás gyógyulási időzítő

**Hallgató:** Ballása Nikolett  
**Neptunkód:** GX5Y1V

**Alcíme:** Grafikus Python alkalmazás friss tetoválások napi ápolásának és gyógyulási fázisainak követésére.

## A projekt rövid bemutatása

A Tetoválás gyógyulási időzítő egy Tkinterrel készített alkalmazás, amely a friss tetoválás óta eltelt napok nyomon követését segíti. A felhasználó beírhatja az eltelt napok számát, vagy megadhatja a tetoválás dátumát, amelyből a program kiszámítja a napok számát. Megjelenik a megfelelő gyógyulási szakasz, az általános ápolási információ és a felhasználó által gombbal kiválasztott bőrállapotra vonatkozó visszajelzés. Rövid saját megjegyzést is lehet szöveges naplóba menteni.

A három gyógyulási szakasz oktatási célú, egyszerűsített felosztás. Az alkalmazás **nem orvosi diagnosztikai eszköz**; a valós ápolásnál a tetováló útmutatása, aggasztó tüneteknél pedig az orvosi tanács az irányadó.

## A program funkciói

1. **Nap megadása és lekérdezés.** Az „Eltelt napok” `Entry` mezőbe 0–3650 közötti egész szám írható. A „Lekérdezés” gomb ellenőrzi és megjeleníti az eredményt.
2. **Napok léptetése.** A „− Előző nap” és a „+ Következő nap” gombok egyesével módosítják a napot. A program azonnal frissíti a feliratokat, és nem lépi át a 0–3650 közötti tartományt.
3. **Számítás dátumból.** A tetoválás dátuma `ÉÉÉÉ-HH-NN` formában adható meg. A `datetime` modul `date` osztálya kiszámítja a mai naphoz viszonyított eltelt napokat. A hibás, jövőbeli vagy 3650 napnál régebbi dátumot elutasítja.
4. **Három gyógyulási szakasz.** 0–3. nap: friss tetoválás; 4–10. nap: hámlás és viszketés; 11. naptól: további regenerálódás. Mindegyikhez általános ápolási szöveg tartozik.
5. **Bőrállapot megadása gombokkal.** Három gomb használható: „Enyhén érzékeny / piros”, „Hámlik / viszket”, „Erősen fáj / terjed a pirosság”. Kattintás után a kiválasztott állapot és a hozzá tartozó szöveg rögtön megjelenik. **Nincs legördülő lista vagy Combobox.**
6. **Személyes megjegyzés mentése.** Egy rövid megjegyzés hozzáfűzhető a `tetovalas_naplo.txt` fájlhoz. A sor tartalmazza a mentés dátumát, a kiválasztott gyógyulási napot, az állapotot és a megjegyzést. Üres bejegyzést nem ment.
7. **Alaphelyzet.** A nap visszaáll 0-ra, az állapot „Nincs kiválasztva” lesz, és a dátum-, illetve megjegyzésmező kiürül. A korábban mentett naplófájlt nem törli.
8. **Kilépés.** Bezárja az alkalmazás ablakát.
9. **Hibakezelés.** Hibás nap vagy dátum, üres megjegyzés, illetve fájlmentési hiba esetén a program figyelmeztető vagy hibaablakot jelenít meg.

Az ablak alján **csak az „Alaphelyzet” és a „Kilépés” gomb** helyezkedik el. A programban nincs külső tájékoztatót vagy böngészőt megnyitó gomb.

## A program felépítése


A `tetovalas_naplo.txt` fájlt az első sikeres mentés hozza létre, ezért a leadandó projektbe nem szükséges előre elkészíteni. Nincs külön tesztmodul vagy tesztfájl. A két Python-fájlban nincs komment.

### 1. main.py – grafikus felület és eseménykezelés

A `TetovalasApp` osztály elkészíti a főablak tartalmát: címeket, `ttk.LabelFrame` és `ttk.Frame` kereteket, `Label` feliratokat, `Entry` mezőket és `Button` gombokat. A gombok `command=` paraméterei a megfelelő metódusra mutatnak. A metódusok a saját adatkezelő osztályt hívják meg, majd a `nezet_frissitese()` a `bn_frissites()` által visszaadott adatokat megjeleníti.

A Python a fájl első sorától feldolgozza az importokat és a definíciókat; az alkalmazást a fenti blokk indítja el, ha a `main.py`-t közvetlenül futtatjuk. A `mainloop()` ezután figyeli a felhasználói eseményeket.

### 2. sajat_modul_bn.py – saját adatkezelő modul

A `TetovalasKezeloBN` osztály tárolja a napot, a dátumot és a kiválasztott állapotot. Az ellenőrzést, a dátumszámítást, a napléptetést, az állapotválasztást, az alaphelyzet visszaállítását és a naplómentést metódusok végzik. A saját `bn_elso_fuggveny()`, `bn_masodik_fuggveny()`, `bn_harmadik_fuggveny()` és `bn_allapot_fuggveny()` függvények részt vesznek a gyógyulási szövegek összeállításában. A `bn_frissites()` egy szótárban adja vissza a felület számára szükséges értékeket.

### A választott új modul: pathlib

A `pathlib` Python szabványos modul, ezért nem kell külön telepíteni. A fájlok és mappák elérési útjait **Path objektumokkal** kezeli. A projektben a `sajat_modul_bn.py` 2. sorában importáljuk:

## Saját osztályok és függvények feladatai

### `TetovalasApp` osztály – `main.py`

Ez az osztály a grafikus alkalmazást építi fel és kezeli a felhasználó műveleteit. Az objektum a `self.root` változóban a főablakra, a `self.kezelo` változóban a gyógyulási adatokat kezelő objektumra hivatkozik. Emellett eltárolja a felület elemeit is: például a beviteli mezőket (`self.nap_entry`, `self.datum_entry`, `self.naplo_entry`), az eredményfeliratokat és a gombokat. Ezek nem a napló tartalmát tárolják, hanem a képernyőn megjelenő elemeket.

- `__init__()`: eltárolja a főablakot, létrehozza az adatkezelő példányt, beállítja az ablak méretét, majd felépíti és frissíti a felületet.
- `felulet_letrehozasa()`: elhelyezi a feliratokat, kereteket, beviteli mezőket és gombokat; összeköti a gombnyomásokat a metódusokkal.
- `nezet_frissitese()`: elkéri a saját modulból az aktuális szövegeket, és beírja őket a megfelelő grafikus elemekbe.
- `lekerdezes()`, `datum_lekerdezes()`: a beírt napot vagy dátumot továbbítja az adatkezelőnek, és szükség esetén figyelmeztetést mutat.
- `kovetkezo_nap()`, `elozo_nap()`: egy nappal lépteti a kiválasztást, majd frissíti a kijelzést.
- `enyhe_kattintas()`, `hamlas_kattintas()`, `problema_kattintas()`: a három állapotgomb eseménykezelői; az `allapot_beallitasa()` metódust hívják meg.
- `allapot_beallitasa()`: átadja a választott állapot számát az adatkezelőnek.
- `naplo_mentes()`: elkéri a megjegyzést, elindítja a fájlmentést, majd siker- vagy hibaüzenetet jelenít meg.
- `alaphelyzet()`: visszaállítja az adatkezelőt, törli a beviteli mezők tartalmát és frissíti a felületet.

### `TetovalasKezeloBN` osztály – `sajat_modul_bn.py`

Ez az osztály a program aktuális gyógyulási adatait tárolja. A `self.nap` az eltelt napok száma, a `self.allapot` a kiválasztott állapot sorszáma (0–3), a `self.datum` a tetoválás dátuma vagy `None`, a `self.statusz` pedig a „Gyógyulási folyamat” felirat. A megjegyzéseket nem az objektum őrzi meg tartósan: azok külön szövegfájlba kerülnek.

- `__init__()`: beállítja a fenti kezdeti adatokat.
- `bn_szuro_adatok()`: a nap alapján visszaadja a megfelelő ápolási tanácsot.
- `bn_ellenorzes()`: ellenőrzi, hogy a beírt érték 0 és `max_nap` közötti egész szám-e.
- `bn_nap_beallitasa()`: érvényes napot állít be, és kézi napválasztásra vált.
- `bn_datum_beallitasa()`: ellenőrzi a megadott dátumot, kiszámítja az eltelt napokat, és eltárolja a dátumot.
- `bn_kovetkezo_nap()`, `bn_elozo_nap()`: módosítja a tárolt napot a megengedett határok között.
- `bn_allapot_valasztas()`: eltárolja a választott állapot számát, ha az érvényes.
- `bn_alaphelyzet()`: visszaállítja az alapadatokat.
- `bn_naplo_mentes()`: a dátumot, a napot, az állapotot és a megjegyzést hozzáfűzi a naplófájlhoz.

### Önálló függvények – `sajat_modul_bn.py`

Ezek nem az osztályba tartozó metódusok, hanem külön meghívható függvények. Egy-egy részfeladatot végeznek el, és visszaadják az eredményt:

- `bn_elso_fuggveny(nap)`: megadja, hogy a kiválasztott nap melyik gyógyulási szakaszhoz tartozik.
- `bn_masodik_fuggveny(szoveg)`: eltávolítja a szöveg elejéről és végéről a felesleges szóközöket.
- `bn_harmadik_fuggveny(napok_szama)`: a nap értékét a megengedett tartományon belül tartja.
- `bn_allapot_fuggveny(allapot)`: visszaadja a választott bőrállapothoz tartozó figyelmeztető vagy tájékoztató szöveget.
- `bn_frissites(kezelo)`: összegyűjti az aktuális napot, gyógyulási szakaszt, ápolási tanácsot, állapotot és dátumszöveget, és egy szótárban visszaadja a grafikus felületnek.

### A saját modulban tárolt közös adatok

- `max_nap = 3650`: a megengedett legnagyobb napszám.
- `allapotok`: a három választható bőrállapot neve és a „Nincs kiválasztva” szöveg egy listában.
- `naplo_fajl`: `Path` objektum, amely megadja, hol található vagy jön létre a `tetovalas_naplo.txt`.

## Futtatás

1. A `main.py` és a `sajat_modul_bn.py` legyen ugyanabban a mappában.
2. Python 3 és működő Tkinter környezet szükséges; külön `pip install` nem kell.
3. Indítás a fejlesztőkörnyezetből vagy terminálból: `python main.py`.
4. Válassz napot vagy adj meg dátumot, majd szükség esetén kattints az egyik állapotgombra.
5. Írhatsz megjegyzést, amelyet a „Mentés” gomb a naplófájl végéhez fűz.
6. Az „Alaphelyzet” visszaállítja a felület aktuális állapotát, a „Kilépés” bezárja az alkalmazást.
