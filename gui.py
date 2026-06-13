import os
import threading
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from modul_git import przygotuj_liste_zmian
from modul_llm import generuj_release_notes


class ModernReleaseNotesGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Release Notes Generator")
        self.root.geometry("600x750")
        self.root.configure(bg="#0f111a")

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('.', background='#0f111a', foreground='#b0b5db', font=('Trebuchet MS', 10))
        self.style.configure('TLabel', background='#0f111a', foreground='#b0b5db')
        self.style.configure('TLabelframe', background='#0f111a', foreground='#b0b5db', bordercolor='#3f4063')
        self.style.configure('TLabelframe.Label', background='#0f111a', foreground='#7ed5ea',
                             font=('Trebuchet MS', 10, 'bold'))

        self.style.configure('Action.TButton', font=('Trebuchet MS', 11, 'bold'), background='#7ed5ea',
                             foreground='#0f111a')
        self.style.map('Action.TButton', background=[('active', '#b0b5db')])

        self.style.configure('Save.TButton', font=('Trebuchet MS', 10, 'bold'), background='#c792ea',
                             foreground='#0f111a')
        self.style.map('Save.TButton', background=[('active', '#b0b5db')])

        self.stworz_interfejs()

    def stworz_interfejs(self):
        glowny = ttk.Frame(self.root, padding="15")
        glowny.pack(fill=tk.BOTH, expand=True)

        ramka_konfig = ttk.LabelFrame(glowny, text=" KONFIGURACJA REPOZYTORIUM ", padding="12")
        ramka_konfig.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(ramka_konfig, text="URL repozytorium lub ścieżka lokalna:").pack(anchor=tk.W)
        self.repo_var = tk.StringVar(value="https://github.com/psf/requests")
        ramka_sciezki = ttk.Frame(ramka_konfig)
        ramka_sciezki.pack(fill=tk.X, pady=(2, 10))

        opcje_entry = {"bg": "#1e1e2f", "fg": "#b0b5db", "insertbackground": "#7ed5ea", "bd": 1, "relief": tk.SOLID}
        self.repo_entry = tk.Entry(ramka_sciezki, textvariable=self.repo_var, **opcje_entry, font=('Trebuchet MS', 10))
        self.repo_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5), ipady=3)

        ttk.Button(ramka_sciezki, text="Wybierz folder", command=self.wybierz_folder).pack(side=tk.RIGHT)

        ramka_zakresorw = ttk.Frame(ramka_konfig)
        ramka_zakresorw.pack(fill=tk.X)

        ttk.Label(ramka_zakresorw, text="Od (np. HEAD~5):").grid(row=0, column=0, sticky=tk.W)
        self.od_var = tk.StringVar(value="HEAD~5")
        self.od_entry = tk.Entry(ramka_zakresorw, textvariable=self.od_var, **opcje_entry)
        self.od_entry.grid(row=1, column=0, sticky=tk.EW, padx=(0, 5), ipady=3)

        ttk.Label(ramka_zakresorw, text="Do (np. HEAD):").grid(row=0, column=1, sticky=tk.W)
        self.do_var = tk.StringVar(value="HEAD")
        self.do_entry = tk.Entry(ramka_zakresorw, textvariable=self.do_var, **opcje_entry)
        self.do_entry.grid(row=1, column=1, sticky=tk.EW, padx=(5, 0), ipady=3)
        ramka_zakresorw.columnconfigure(0, weight=1)
        ramka_zakresorw.columnconfigure(1, weight=1)

        self.btn_generuj = ttk.Button(glowny, text=" GENERUJ RELEASE NOTES", style='Action.TButton',
                                      command=self.start_generowania)
        self.btn_generuj.pack(fill=tk.X, ipady=6, pady=(5, 5))

        self.status_var = tk.StringVar(value="Gotowy.")
        ttk.Label(glowny, textvariable=self.status_var, font=('Trebuchet MS', 9, 'italic'), foreground='#b0b5db').pack(
            anchor=tk.W, pady=(0, 15))

        ttk.Label(glowny, text="PODGLĄD WYNIKU (MARKDOWN):", font=('Trebuchet MS', 9, 'bold'),
                  foreground='#7ed5ea').pack(anchor=tk.W, pady=(0, 5))

        self.txt_podglad = tk.Text(glowny, wrap=tk.WORD, font=('Consolas', 10), bg="#1e1e2f", fg="#7ed5ea",
                                   insertbackground="#7ed5ea", bd=1, relief=tk.SOLID, padx=10, pady=10)
        self.txt_podglad.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        self.btn_zapisz = ttk.Button(glowny, text=" Zapisz jako plik Markdown (.md)", style='Save.TButton',
                                     command=self.zapisz_plik)
        self.btn_zapisz.pack(fill=tk.X, ipady=5)

    def wybierz_folder(self):
        katalog = filedialog.askdirectory()
        if katalog: self.repo_var.set(katalog)

    def start_generowania(self):
        self.btn_generuj.config(state=tk.DISABLED)
        self.status_var.set("Trwa generowanie... Pobieranie danych z Git i LLM.")
        self.txt_podglad.delete("1.0", tk.END)
        threading.Thread(target=self.proces_generowania, daemon=True).start()

    def proces_generowania(self):
        try:
            lista_zmian = przygotuj_liste_zmian(self.repo_var.get().strip(), self.od_var.get().strip(),
                                                self.do_var.get().strip())
            if not lista_zmian:
                self.koniec_pracy("Nie znaleziono commitów.", sukces=False)
                return

            wynik = generuj_release_notes(lista_zmian)
            self.root.after(0, lambda: self.txt_podglad.insert(tk.END, wynik))
            self.koniec_pracy(f"Generowanie zakończone sukcesem! (Commity: {len(lista_zmian)})", sukces=True)
        except Exception as e:
            self.koniec_pracy(f"Błąd: {str(e)}", sukces=False)

    def koniec_pracy(self, komunikat, sukces):
        self.root.after(0, lambda: self._odswiez_ui(komunikat, sukces))

    def _odswiez_ui(self, komunikat, sukces):
        self.btn_generuj.config(state=tk.NORMAL)
        self.status_var.set(komunikat)
        if not sukces: messagebox.showerror("Błąd", komunikat)

    def zapisz_plik(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernReleaseNotesGUI(root)
    root.mainloop()