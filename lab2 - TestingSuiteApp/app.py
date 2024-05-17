import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.stats import linregress

class AplikacjaCSV:
    def __init__(self, root):
        self.okno_glowne = root
        self.okno_glowne.title("Inżynieria testów oraz jakości - Zad 2.")
        
        # Inicjalizacja jako None:
        self.dane = None
        self.figura = None
        self.aktualny_wykres = None
        self.typ_skali = 'liniowa'

        self.utworz_elementy_interfejsu()

    def utworz_elementy_interfejsu(self):
        # Ramka na tabelę i wykres
        self.ramka_danych = tk.Frame(self.okno_glowne)
        self.ramka_danych.pack()

        self.pole_tekstowe = scrolledtext.ScrolledText(self.ramka_danych, width=50, height=20)
        self.pole_tekstowe.pack(side=tk.LEFT, padx=5, pady=5)

        self.ramka_wykresu = tk.Frame(self.ramka_danych)
        self.ramka_wykresu.pack(side=tk.LEFT, padx=5, pady=5)

        # Przyciski
        self.przycisk_wczytaj = tk.Button(self.okno_glowne, text="Wczytaj plik CSV", command=self.wczytaj_csv)
        self.przycisk_wczytaj.pack(pady=5)

        self.przycisk_wykresu = tk.Button(self.okno_glowne, text="Generuj Wykres", command=self.generuj_wykres)
        self.przycisk_wykresu.pack(side=tk.LEFT, padx=5, pady=5)

        self.przycisk_skali = tk.Button(self.okno_glowne, text="Zmień Skalę", command=self.zmien_skale)
        self.przycisk_skali.pack(side=tk.LEFT, padx=5, pady=5)

        self.przycisk_regresji = tk.Button(self.okno_glowne, text="Oblicz Regresję", command=self.oblicz_regresje)
        self.przycisk_regresji.pack(side=tk.LEFT, padx=5, pady=5)

    def wczytaj_csv(self):
        sciezka_do_pliku = filedialog.askopenfilename(filetypes=[("Pliki CSV", "*.csv")])
        if sciezka_do_pliku: # czy użytkownik wybrał plik.
            try:
                self.dane = pd.read_csv(sciezka_do_pliku, sep=';')
                self.pole_tekstowe.delete(1.0, tk.END) # tk.END - stała określająca koniec tekstu w scrolledtext.
                self.pole_tekstowe.insert(tk.END, self.dane.to_string(index=False)) # umieszczenie danych w scrolledtext.
            except Exception as e:
                messagebox.showerror("Błąd", f"Błąd podczas wczytywania pliku CSV:\n{e}")

    def generuj_wykres(self):
        if self.dane is not None and not self.dane.empty: # czy dane wczytane i czy nie puste.
            if self.aktualny_wykres: # miejsce na wykres.
                self.aktualny_wykres.get_tk_widget().destroy()

            self.figura, osie = plt.subplots()
            osie.plot(self.dane.iloc[:, 0], self.dane.iloc[:, 1], label='Dane') #
            osie.set_xlabel('Oś X')
            osie.set_ylabel('Oś Y')
            osie.set_title('Wykres danych')
            

            if self.typ_skali == 'logarytmiczna':
                osie.set_yscale('log')

            
            # Dodanie linii regresji
            if self.dane is not None and not self.dane.empty:
                x = self.dane.iloc[:, 0] # przypisanie pierwszej kolumny do zmiennej x.
                y = self.dane.iloc[:, 1] # przypisanie drugiej kolumny do zmiennej y.
                slope, intercept, _, _, _ = linregress(x, y)
                regresja = slope * x + intercept
                osie.plot(x, regresja, label='Linia regresji', color='red')


            osie.legend()
            canvas = FigureCanvasTkAgg(self.figura, master=self.ramka_wykresu)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            self.aktualny_wykres = canvas

    def zmien_skale(self):
        if self.typ_skali == 'liniowa':
            self.typ_skali = 'logarytmiczna'
        else:
            self.typ_skali = 'liniowa'
        self.generuj_wykres()

    def oblicz_regresje(self):
        if self.dane is not None and not self.dane.empty:
            x = self.dane.iloc[:, 0]
            y = self.dane.iloc[:, 1]
            slope, intercept, _, _, _ = linregress(x, y)
            wynik = f"SLOPE (A): {slope}\nINTERCEPT (B): {intercept}"
            messagebox.showinfo("REGREJA LINIOWA WARTOŚCI:", wynik)

if __name__ == "__main__":
    root = tk.Tk()
    aplikacja = AplikacjaCSV(root)
    root.mainloop()
