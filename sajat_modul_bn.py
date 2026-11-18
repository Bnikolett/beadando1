from datetime import date
from pathlib import Path


max_nap = 3650
naplo_fajl = Path(__file__).resolve().parent / "tetovalas_naplo.txt"

allapotok = [
    "Nincs kiválasztva",
    "Enyhén érzékeny / piros",
    "Hámlik / viszket",
    "Erősen fáj / terjed a pirosság"
]


def bn_elso_fuggveny(nap):
    if nap <= 3:
        return "1. szakasz – Friss tetoválás (0–3. nap)"
    elif nap <= 10:
        return "2. szakasz – Hámlás és viszketés (4–10. nap)"
    else:
        return "3. szakasz – További regenerálódás (11. naptól)"


def bn_masodik_fuggveny(szoveg):
    return szoveg.strip()


def bn_harmadik_fuggveny(napok_szama):
    if napok_szama < 0:
        return 0
    if napok_szama > max_nap:
        return max_nap
    return napok_szama


def bn_allapot_fuggveny(allapot):
    if allapot == 1:
        return (
            "Az enyhe érzékenység előfordulhat. "
            "Ha a panasz fokozódik vagy nem javul, kérj orvosi tanácsot."
        )
    elif allapot == 2:
        return (
            "A hámlás és a viszketés a gyógyulás része lehet. "
            "Ne vakard, és ne húzd le a hámló bőrt."
        )
    elif allapot == 3:
        return (
            "Az erősödő fájdalom és a terjedő pirosság fertőzés jele is lehet. "
            "Fordulj mielőbb orvoshoz!"
        )
    return "Válassz ki egy bőrállapotot a részletes visszajelzéshez."


def bn_frissites(kezelo):
    nap = bn_harmadik_fuggveny(kezelo.nap)
    szakasz = bn_elso_fuggveny(nap)
    apolas = bn_masodik_fuggveny(kezelo.bn_szuro_adatok(nap))
    allapot_nev = allapotok[kezelo.allapot]
    visszajelzes = bn_allapot_fuggveny(kezelo.allapot)
    if kezelo.datum is None:
        datum_szoveg = "Kézi napválasztás"
    else:
        datum_szoveg = "Tetoválás dátuma: " + kezelo.datum.isoformat()
    return {
        "nap": nap,
        "szakasz": szakasz,
        "apolas": apolas,
        "allapot": allapot_nev,
        "visszajelzes": visszajelzes,
        "datum": datum_szoveg
    }


class TetovalasKezeloBN:
    def __init__(self):
        self.statusz = "Gyógyulási folyamat"
        self.nap = 0
        self.allapot = 0
        self.datum = None

    def bn_szuro_adatok(self, nap):
        if nap <= 3:
            return (
                "Ápolás: kíméletes tisztítás, tiszta kéz és "
                "a tetováló által javasolt utóápolás."
            )
        elif nap <= 10:
            return (
                "Ápolás: a hámló bőr kímélése, óvatos tisztítás "
                "és szükség szerint vékony hidratálás."
            )
        return (
            "Ápolás: tartsd tisztán és hidratáltan a bőrt. "
            "A mélyebb rétegek regenerálódása tovább tarthat."
        )

    def bn_ellenorzes(self, ertek):
        try:
            szam = int(ertek.strip())
            return 0 <= szam <= max_nap
        except (ValueError, AttributeError):
            return False

    def bn_nap_beallitasa(self, ertek):
        if not self.bn_ellenorzes(ertek):
            return False
        self.nap = int(ertek.strip())
        self.datum = None
        return True

    def bn_datum_beallitasa(self, ertek):
        try:
            szoveg = ertek.strip()
            if len(szoveg) != 10 or szoveg[4] != "-" or szoveg[7] != "-":
                return False
            kivalasztott_datum = date.fromisoformat(szoveg)
        except (ValueError, AttributeError):
            return False
        napok = (date.today() - kivalasztott_datum).days
        if napok < 0 or napok > max_nap:
            return False
        self.datum = kivalasztott_datum
        self.nap = napok
        return True

    def bn_kovetkezo_nap(self):
        if self.nap < max_nap:
            self.nap = self.nap + 1
        self.datum = None

    def bn_elozo_nap(self):
        if self.nap > 0:
            self.nap = self.nap - 1
        self.datum = None

    def bn_allapot_valasztas(self, allapot):
        if 0 <= allapot < len(allapotok):
            self.allapot = allapot

    def bn_alaphelyzet(self):
        self.nap = 0
        self.allapot = 0
        self.datum = None

    def bn_naplo_mentes(self, megjegyzes):
        megjegyzes = megjegyzes.strip()
        if megjegyzes == "":
            return False
        adat = bn_frissites(self)
        szoveg = (
            "Rögzítés: " + date.today().isoformat() + " | "
            "Nap: " + str(adat["nap"]) + " | "
            "Állapot: " + adat["allapot"] + " | "
            "Megjegyzés: " + megjegyzes.replace("\n", " ") + "\n"
        )
        with naplo_fajl.open("a", encoding="utf-8") as fajl:
            fajl.write(szoveg)
        return True
