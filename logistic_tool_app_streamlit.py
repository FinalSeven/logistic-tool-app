import streamlit as st
from PIL import Image
import time
from playwright.sync_api import sync_playwright

st.set_page_config(page_title="Gefahrstoff-Label-Suche", page_icon="🚚", layout="centered")

# BMW-Farben
BMW_BLUE = "#1c69d4"
BMW_WHITE = "#ffffff"
BMW_BLACK = "#000000"
BMW_GREEN = "#3EA83E"

# Logos anzeigen
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    try:
        st.image("bmw_logo.png", width=80)
    except:
        pass
with col3:
    try:
        st.image("mini_logo.png", width=120)
    except:
        pass

st.markdown("<h2 style='text-align:center;color:black;'>Gefahrstoff-Label-Suche</h2>", unsafe_allow_html=True)
st.write("Classification, Labelling and Packaging (CLP) of substances and mixtures")

teilenummer = st.text_input("🔢 Teilenummer", placeholder="Teilenummer eingeben (7 oder 11 Zeichen)")
land = st.text_input("🌍 Land", placeholder="z. B. DE, Deutschland, FR, etc.")

start = st.button("🚀 Start")

if start:
    if len(teilenummer) not in [7, 11]:
        st.warning("⚠️ Teilenummer muss 7 oder 11 Zeichen lang sein!")
    elif not land.strip():
        st.warning("⚠️ Land darf nicht leer sein!")
    else:
        with st.spinner("Starte Workflow..."):
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto("https://finalseven.github.io/logistic-tool/")
                page.fill("#part", teilenummer)
                page.select_option("#country", land.strip().lower())
                page.wait_for_timeout(2000)
                st.success(f"✅ Workflow für {teilenummer} / {land} abgeschlossen!")
                browser.close()
