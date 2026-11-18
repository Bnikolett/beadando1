import tkinter as tk
from tkinter import ttk, messagebox

from sajat_modul_bn import (
    max_nap,
    TetovalasKezeloBN,
    bn_frissites
)


class TetovalasApp:
    def __init__(self, root):
        self.root = root
        self.kezelo = TetovalasKezeloBN()
        self.root.title("Tetoválás gyógyulási időzítő")
        self.root.geometry("780x665")
        self.root.minsize(700, 620)
        self.felulet_letrehozasa()
        self.nezet_frissitese()

    def felulet_letrehozasa(self):
        self.focim = ttk.Label(
            self.root,
            text="Tetoválás gyógyulási időzítő",
            font=("Arial", 19, "bold")
        )
        self.focim.pack(pady=10)

        self.alcim = ttk.Label(
            self.root,
            text="Napi ápolás és személyes követés",
            font=("Arial", 10)
        )
        self.alcim.pack(pady=2)

        self.nap_keret = ttk.LabelFrame(self.root, text="Nap kiválasztása")
        self.nap_keret.pack(fill="x", padx=16, pady=7)

        self.nap_sor = ttk.Frame(self.nap_keret)
        self.nap_sor.pack(pady=7)

        self.nap_felirat = ttk.Label(self.nap_sor, text="Eltelt napok:")
        self.nap_felirat.pack(side="left", padx=5)

        self.nap_entry = ttk.Entry(self.nap_sor, width=10)
        self.nap_entry.insert(0, "0")
        self.nap_entry.pack(side="left", padx=5)

        self.lekerdezes_gomb = ttk.Button(
            self.nap_sor, text="Lekérdezés", command=self.lekerdezes
        )
        self.lekerdezes_gomb.pack(side="left", padx=5)

        self.minusz_gomb = ttk.Button(
            self.nap_sor, text="− Előző nap", command=self.elozo_nap
        )
        self.minusz_gomb.pack(side="left", padx=5)

        self.plusz_gomb = ttk.Button(
            self.nap_sor, text="+ Következő nap", command=self.kovetkezo_nap
        )
        self.plusz_gomb.pack(side="left", padx=5)

        self.datum_sor = ttk.Frame(self.nap_keret)
        self.datum_sor.pack(pady=7)

        self.datum_felirat = ttk.Label(
            self.datum_sor, text="Tetoválás dátuma (ÉÉÉÉ-HH-NN):"
        )
        self.datum_felirat.pack(side="left", padx=5)

        self.datum_entry = ttk.Entry(self.datum_sor, width=16)
        self.datum_entry.pack(side="left", padx=5)

        self.datum_gomb = ttk.Button(
            self.datum_sor, text="Napok kiszámítása", command=self.datum_lekerdezes
        )
        self.datum_gomb.pack(side="left", padx=5)

        self.allapot_keret = ttk.LabelFrame(self.root, text="A tetoválás állapota")
        self.allapot_keret.pack(fill="x", padx=16, pady=7)

        self.allapot_gomb_sor = ttk.Frame(self.allapot_keret)
        self.allapot_gomb_sor.pack(pady=6)

        self.enyhe_gomb = ttk.Button(
            self.allapot_gomb_sor,
            text="Enyhén érzékeny / piros",
            command=self.enyhe_kattintas
        )
        self.enyhe_gomb.pack(side="left", padx=4)

        self.hamlas_gomb = ttk.Button(
            self.allapot_gomb_sor,
            text="Hámlik / viszket",
            command=self.hamlas_kattintas
        )
        self.hamlas_gomb.pack(side="left", padx=4)

        self.problema_gomb = ttk.Button(
            self.allapot_gomb_sor,
            text="Erősen fáj / terjed a pirosság",
            command=self.problema_kattintas
        )
        self.problema_gomb.pack(side="left", padx=4)

        self.eredmeny_keret = ttk.LabelFrame(self.root, text="Gyógyulási információk")
        self.eredmeny_keret.pack(fill="x", padx=16, pady=7)

        self.nap_label = ttk.Label(
            self.eredmeny_keret, text="", font=("Arial", 15, "bold")
        )
        self.nap_label.pack(pady=4)

        self.datum_label = ttk.Label(self.eredmeny_keret, text="")
        self.datum_label.pack(pady=2)

        self.szakasz_label = ttk.Label(
            self.eredmeny_keret, text="", font=("Arial", 12, "bold")
        )
        self.szakasz_label.pack(pady=4)

        self.apolas_label = tk.Label(
            self.eredmeny_keret, text="", wraplength=700, justify="center"
        )
        self.apolas_label.pack(pady=5)

        self.allapot_label = ttk.Label(
            self.eredmeny_keret, text="", font=("Arial", 10, "bold")
        )
        self.allapot_label.pack(pady=3)

        self.visszajelzes_label = tk.Label(
            self.eredmeny_keret, text="", wraplength=700, justify="center"
        )
        self.visszajelzes_label.pack(pady=5)

        self.naplo_keret = ttk.LabelFrame(self.root, text="Saját megjegyzés")
        self.naplo_keret.pack(fill="x", padx=16, pady=7)

        self.naplo_sor = ttk.Frame(self.naplo_keret)
        self.naplo_sor.pack(pady=8)

        self.naplo_entry = ttk.Entry(self.naplo_sor, width=63)
        self.naplo_entry.pack(side="left", padx=5)

        self.mentes_gomb = ttk.Button(
            self.naplo_sor, text="Mentés", command=self.naplo_mentes
        )
        self.mentes_gomb.pack(side="left", padx=5)

        self.also_sor = ttk.Frame(self.root)
        self.also_sor.pack(pady=8)

        self.reset_gomb = ttk.Button(
            self.also_sor, text="Alaphelyzet", command=self.alaphelyzet
        )
        self.reset_gomb.pack(side="left", padx=7)

        self.kilepes_gomb = ttk.Button(
            self.also_sor, text="Kilépés", command=self.root.destroy
        )
        self.kilepes_gomb.pack(side="left", padx=7)

    def nezet_frissitese(self):
        adatok = bn_frissites(self.kezelo)
        self.nap_label.config(text="Kiválasztott nap: " + str(adatok["nap"]))
        self.datum_label.config(text=adatok["datum"])
        self.szakasz_label.config(text=adatok["szakasz"])
        self.apolas_label.config(text=adatok["apolas"])
        self.allapot_label.config(text="Állapot: " + adatok["allapot"])
        self.visszajelzes_label.config(text=adatok["visszajelzes"])
        self.nap_entry.delete(0, tk.END)
        self.nap_entry.insert(0, str(adatok["nap"]))

    def lekerdezes(self):
        if not self.kezelo.bn_nap_beallitasa(self.nap_entry.get()):
            messagebox.showwarning(
                "Hibás nap", "0 és " + str(max_nap) + " közötti egész számot adj meg!"
            )
            return
        self.nezet_frissitese()

    def datum_lekerdezes(self):
        if not self.kezelo.bn_datum_beallitasa(self.datum_entry.get()):
            messagebox.showwarning(
                "Hibás dátum", "Érvényes, nem jövőbeli dátumot adj meg ÉÉÉÉ-HH-NN formában!"
            )
            return
        self.nezet_frissitese()

    def kovetkezo_nap(self):
        self.kezelo.bn_kovetkezo_nap()
        self.nezet_frissitese()

    def elozo_nap(self):
        self.kezelo.bn_elozo_nap()
        self.nezet_frissitese()

    def enyhe_kattintas(self):
        self.allapot_beallitasa(1)

    def hamlas_kattintas(self):
        self.allapot_beallitasa(2)

    def problema_kattintas(self):
        self.allapot_beallitasa(3)

    def allapot_beallitasa(self, allapot):
        self.kezelo.bn_allapot_valasztas(allapot)
        self.nezet_frissitese()

    def naplo_mentes(self):
        try:
            siker = self.kezelo.bn_naplo_mentes(self.naplo_entry.get())
        except OSError:
            messagebox.showerror("Mentési hiba", "Nem sikerült elmenteni a megjegyzést.")
            return
        if not siker:
            messagebox.showwarning("Üres megjegyzés", "Írj be egy megjegyzést a mentéshez!")
            return
        messagebox.showinfo("Mentés", "A megjegyzés a tetovalas_naplo.txt fájlba került.")
        self.naplo_entry.delete(0, tk.END)

    def alaphelyzet(self):
        self.kezelo.bn_alaphelyzet()
        self.datum_entry.delete(0, tk.END)
        self.naplo_entry.delete(0, tk.END)
        self.nezet_frissitese()


if __name__ == "__main__":
    fo_ablak = tk.Tk()
    app = TetovalasApp(fo_ablak)
    fo_ablak.mainloop()
