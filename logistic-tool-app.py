import tkinter as tk
from tkinter import messagebox
import threading
import time
import os
from PIL import Image, ImageTk
from playwright.sync_api import sync_playwright
import pyautogui
import pygetwindow as gw

# Länder-Definition inklusive Kürzel und ausgeschrieben
COUNTRY_MAP = {
    "DE": ["de"], "Deutschland": ["de"],
    "BE": ["be"], "Belgien": ["be"],
    "FI": ["fr"], "Frankreich": ["fr"],
    "FR": ["fi"], "Finnland": ["fi"],
    "BG": ["bg"], "Bulgarien": ["bg"],
    "CN": ["cn"], "China": ["cn"],
    "DK": ["dk"], "Dänemark": ["dk"],
    "EE": ["ee"], "Estland": ["ee"],
    "LV": ["lv"], "Lettland": ["lv"],
    "LT": ["lt"], "Litauen": ["lt"],
    "MT": ["mt"], "Malta": ["mt"],
    "NL": ["nl"], "Niederlande": ["nl"],
    "NO": ["no"], "Norwegen": ["no"],
    "AT": ["at"], "Oesterreich": ["at"],
    "AT": ["at"], "Österreich": ["at"],
    "GR": ["gr"], "Griechenland": ["gr"],
    "IE": ["ie"], "Irland": ["ie"],
    "IT": ["it"], "Italien": ["it"],
    "US": ["us"], "USA": ["us"],
    "HR": ["hr"], "Kroatien": ["hr"],
    "CA": ["ca"], "Kanada": ["ca"],
    "KR": ["kr"], "Korea": ["kr"],
    "JP": ["jp"], "Japan": ["jp"],
    "PL": ["pl"], "Polen": ["pl"],
    "PT": ["pt"], "Portugal": ["pt"],
    "RO": ["ro"], "Rumaenien": ["ro"],
    "RO": ["ro"], "Rumänien": ["ro"],
    "RU": ["ru"], "Russland": ["ru"],
    "CY": ["cy"], "Republik Zypern": ["cy"],
    "CH": ["ch"], "Schweiz": ["ch"],
    "SE": ["se"], "Schweden": ["se"],
    "ES": ["es"], "Spanien": ["es"],
    "SK": ["sk"], "Slowakei": ["sk"],
    "SL": ["sl"], "Slowenien": ["sl"],
    "CZ": ["cz"], "Tschechien": ["cz"],
    "TR": ["tr"], "Tuerkei": ["tr"],
    "TR": ["tr"], "Türkei": ["tr"],
    "HU": ["hu"], "Ungarn": ["hu"],
    "GB": ["gb"], "Vereinigtes Koenigreich": ["gb"],
    "GB": ["gb"], "Vereinigtes Königreich": ["gb"],
    "LU": ["lu"], "Luxemburg": ["lu"]
}

# BMW-Farben
BMW_BLUE = "#1c69d4"
BMW_BLACK = "#000000"
BMW_WHITE = "#ffffff"
BMW_GRAY = "#E5E5E5"
BMW_ORANGE = "#F39C12"
BMW_GREEN = "#3EA83E"
BMW_RED = "#E74C3C"

class LogisticTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Gefahrstoff-Label-Suche")
        self.root.geometry("800x500")
        self.root.configure(bg=BMW_WHITE)
        self.root.resizable(True, True)

        try:
            self.root.iconbitmap("bmw_icon.ico")
        except:
            try:
                if os.path.exists("bmw_logo.png"):
                    icon_img = Image.open("bmw_logo.png").resize((32,32))
                    self.root.iconphoto(True, ImageTk.PhotoImage(icon_img))
            except:
                print("Kein Icon gefunden, Standard wird genutzt.")

        self.escape_pressed = 0
        self.running_animation = False

        self.create_widgets()
        self.bind_events()
        self.configure_grid()

    # --- Widgets ---
    def create_widgets(self):
        self.header_canvas = tk.Canvas(self.root, bg=BMW_WHITE, height=80, highlightthickness=0)
        self.header_canvas.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        self.root.grid_columnconfigure(0, weight=1)

        if os.path.exists("bmw_logo.png"):
            bmw_img = Image.open("bmw_logo.png").resize((40, 40))
            self.bmw_icon = ImageTk.PhotoImage(bmw_img)
            self.bmw_item = self.header_canvas.create_image(0, 0, image=self.bmw_icon, anchor="w")

        if os.path.exists("mini_logo.png"):
            mini_img = Image.open("mini_logo.png").resize((80, 40))
            self.mini_icon = ImageTk.PhotoImage(mini_img)
            self.mini_item = self.header_canvas.create_image(0, 0, image=self.mini_icon, anchor="e")

        self.title_text_item = self.header_canvas.create_text(0, 0, text="Gefahrstoff-Label-Suche",
                                                              font=("Arial", 14, "bold"),
                                                              fill=BMW_BLACK)

        subtitle1_frame = tk.Frame(self.root, bg=BMW_WHITE)
        subtitle1_frame.grid(row=1, column=0, sticky="ew", padx=10)
        subtitle1_text = "Classification, Labelling and Packaging of substances and mixtures"
        subtitle1_text_widget = tk.Text(subtitle1_frame, height=1, bg=BMW_WHITE, bd=0, highlightthickness=0)
        subtitle1_text_widget.pack(fill="x")
        subtitle1_text_widget.tag_configure("red", foreground="red")
        subtitle1_text_widget.insert("1.0", subtitle1_text)
        for idx, char in enumerate(subtitle1_text):
            if char in ['C','L','P']:
                subtitle1_text_widget.tag_add("red", f"1.{idx}", f"1.{idx+1}")
        subtitle1_text_widget.config(state="disabled", font=("Arial",12))
        subtitle1_text_widget.tag_configure("center", justify="center")
        subtitle1_text_widget.tag_add("center", "1.0", "end")

        subtitle2_label = tk.Label(self.root,
                                   text="Verordnung über die Einstufung, Kennzeichnung und Verpackung von Stoffen und Gemischen",
                                   bg=BMW_WHITE, fg=BMW_BLACK, font=("Arial", 12))
        subtitle2_label.grid(row=2, column=0, sticky="ew", padx=10)
        subtitle2_label.configure(anchor="center")

        entry_font = ("Arial", 16)
        self.entry_teilenummer = tk.Entry(self.root, fg="grey", font=entry_font, width=25)
        self.entry_teilenummer.grid(row=3, column=0, sticky="n", pady=10)
        self.set_placeholder(self.entry_teilenummer, "Teilenummer eingeben...")

        self.entry_land = tk.Entry(self.root, fg="grey", font=entry_font, width=25)
        self.entry_land.grid(row=4, column=0, sticky="n", pady=10)
        self.set_placeholder(self.entry_land, "Land eingeben...")

        self.btn_start = tk.Button(self.root, text="Start", bg=BMW_BLUE, fg=BMW_WHITE,
                                   font=("Arial", 12, "bold"), command=self.start_workflow)
        self.btn_start.grid(row=5, column=0, pady=10)
        self.btn_start.bind("<Enter>", lambda e: self.btn_start.config(bg="#2b7cd4"))
        self.btn_start.bind("<Leave>", lambda e: self.btn_start.config(bg=BMW_BLUE))

        self.lbl_status = tk.Label(self.root, text="Bereit für Eingabe", bg=BMW_WHITE, fg=BMW_BLACK)
        self.lbl_status.grid(row=6, column=0, sticky="ew", padx=20, pady=5)

        def resize_header(event):
            width = event.width
            height = event.height
            padding = 10
            if hasattr(self, "bmw_item"):
                self.header_canvas.coords(self.bmw_item, padding, height//2)
            if hasattr(self, "mini_item"):
                self.header_canvas.coords(self.mini_item, width - padding, height//2)
            self.header_canvas.coords(self.title_text_item, width//2, height//2)
            new_size = max(14, min(36, width//20))
            self.header_canvas.itemconfig(self.title_text_item, font=("Arial", new_size, "bold"))

        self.header_canvas.bind("<Configure>", resize_header)
        self.entry_teilenummer.bind("<FocusIn>", lambda e: self.select_all(self.entry_teilenummer))
        self.entry_land.bind("<FocusIn>", lambda e: self.select_all(self.entry_land))

    # --- Grid-Konfiguration ---
    def configure_grid(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight=0)
        for i in range(3,7):
            self.root.grid_rowconfigure(i, weight=1)

    # --- Platzhalter ---
    def set_placeholder(self, entry, text):
        entry.delete(0, tk.END)
        entry.insert(0, text)
        entry.config(fg="grey")
        entry.bind("<FocusIn>", lambda e: self.clear_placeholder(entry, text))
        entry.bind("<FocusOut>", lambda e: self.add_placeholder(entry, text))

    def clear_placeholder(self, entry, text):
        if entry.get() == text and entry.cget("fg") == "grey":
            entry.delete(0, tk.END)
            entry.config(fg="black")

    def add_placeholder(self, entry, text):
        if not entry.get():
            entry.insert(0, text)
            entry.config(fg="grey")

    def select_all(self, entry):
        entry.after(50, lambda: entry.select_range(0, tk.END))

    # --- Bindings ---
    def bind_events(self):
        self.entry_teilenummer.focus()
        self.entry_teilenummer.bind('<Return>', self.on_teilenummer_enter)
        self.entry_land.bind('<Return>', self.on_land_enter)
        self.root.bind('<Escape>', self.on_escape)

    def reset_escape_counter(self):
        self.escape_pressed = 0

    def abort_to_start(self):
        self.running_animation = False
        self.set_placeholder(self.entry_teilenummer, "Teilenummer eingeben...")
        self.set_placeholder(self.entry_land, "Land eingeben...")
        self.entry_teilenummer.focus()
        self.select_all(self.entry_teilenummer)
        self.lbl_status.config(text="Bereit für nächste Eingabe")

    def on_escape(self, event=None):
        self.escape_pressed += 1
        if self.escape_pressed == 1:
            self.lbl_status.config(text="Abbruch! Zur TNR-Eingabe zurück.")
            self.abort_to_start()
            self.root.after(1000, self.reset_escape_counter)
        elif self.escape_pressed >= 2:
            self.root.destroy()

    # --- Workflow ---
    def run_script(self, teilenummer, land_kurz):
        with sync_playwright() as p:
            browser = p.chromium.launch(channel="msedge", headless=False)
            context = browser.new_context()
            page = context.new_page()
            page.goto("https://finalseven.github.io/logistic-tool/")
            page.fill("#part", teilenummer)
            page.select_option("#country", land_kurz)
            page.evaluate("""() => { const e = document.querySelector('#country'); e.dispatchEvent(new Event('change', { bubbles: true })); }""")
            page.wait_for_function("""() => document.querySelectorAll('#lang option').length > 0""")
            gedruckte_sprachen = set()
            while True:
                options = page.eval_on_selector_all("#lang option", "opts => opts.map(o => ({value: o.value, text: o.textContent.trim()}))")
                neue_optionen = [opt for opt in options if opt['value'] and opt['value'] not in gedruckte_sprachen]
                if not neue_optionen:
                    break
                for opt in neue_optionen:
                    sprache_text = opt['text']
                    sprache_value = opt['value']
                    self.lbl_status.config(text=f"Verarbeite Sprache: {sprache_text}", fg=BMW_BLUE)
                    page.select_option("#lang", sprache_value)
                    page.evaluate("""() => { const e = document.querySelector('#lang'); e.dispatchEvent(new Event('change', { bubbles: true })); }""")
                    page.wait_for_timeout(500)
                    page.click(".primary")
                    page.wait_for_selector("#resultsTable")
                    with context.expect_page() as new_page_event:
                        page.locator(".icon:has-text('🚚')").click()
                    pdf_page = new_page_event.value
                    pdf_page.wait_for_load_state("load")
                    pdf_page.bring_to_front()
                    time.sleep(1)
                    try:
                        for w in gw.getAllTitles():
                            if "Edge" in w or "Chromium" in w or "Logistic Tool" in w:
                                win = gw.getWindowsWithTitle(w)[0]
                                win.activate()
                                break
                    except:
                        pass
                    pyautogui.hotkey("ctrl", "p")
                    time.sleep(3)
                    pyautogui.press("enter")
                    time.sleep(1)
                    pdf_page.close()
                    gedruckte_sprachen.add(sprache_value)
            browser.close()
            self.lbl_status.config(text="Workflow abgeschlossen!", fg=BMW_GREEN)
            # --- Fokus zurück auf Teilenummer ---
            self.entry_teilenummer.focus()
            self.select_all(self.entry_teilenummer)

    def start_workflow(self):
        teilenummer = self.entry_teilenummer.get().strip()
        land = self.entry_land.get().strip()
        if not teilenummer or teilenummer == "Teilenummer eingeben..." or len(teilenummer) not in [7, 11]:
            messagebox.showwarning("Fehler", "Teilenummer muss genau 7 oder 11 Zeichen lang sein!")
            self.abort_to_start()
            return
        land_kurz = None
        for key, values in COUNTRY_MAP.items():
            if land.lower() == key.lower() or land.lower() in [v.lower() for v in values]:
                if len(key) == 2:
                    land_kurz = key.upper()
                else:
                    for k, v in COUNTRY_MAP.items():
                        if len(k) == 2 and v == COUNTRY_MAP[key]:
                            land_kurz = k.upper()
                            break
                break
        if not land_kurz:
            messagebox.showwarning("Fehler", f"Ungültiges Land: {land}")
            self.abort_to_start()
            return
        self.entry_land.delete(0, tk.END)
        self.entry_land.insert(0, land_kurz)
        self.btn_start.config(state="disabled")
        self.entry_teilenummer.config(state="normal")
        self.entry_land.config(state="normal")
        self.running_animation = True
        self.animate_status_non_blocking("Workflow läuft", BMW_BLUE)
        threading.Thread(target=lambda: self.run_script(teilenummer, land_kurz)).start()

    def animate_status_non_blocking(self, base_text, color, i=0):
        if not self.running_animation:
            return
        dots = "." * (i % 4)
        self.lbl_status.config(text=f"{base_text}{dots}", fg=color)
        i += 1
        self.root.after(300, lambda: self.animate_status_non_blocking(base_text, color, i))

    def on_teilenummer_enter(self, event=None):
        teilenummer = self.entry_teilenummer.get().strip()
        if not teilenummer or teilenummer == "Teilenummer eingeben..." or len(teilenummer) not in [7, 11]:
            messagebox.showwarning("Fehler", "Teilenummer muss genau 7 oder 11 Zeichen lang sein!")
            self.abort_to_start()
            return
        self.entry_land.focus()
        self.select_all(self.entry_land)

    def on_land_enter(self, event=None):
        self.start_workflow()


if __name__ == "__main__":
    root = tk.Tk()
    app = LogisticTool(root)
    root.mainloop()
