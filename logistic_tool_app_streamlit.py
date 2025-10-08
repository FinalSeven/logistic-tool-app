import streamlit as st
from PIL import Image
import time

# --- Seiteneinstellungen ---
st.set_page_config(page_title="Logistic Tool App", page_icon="🚚", layout="centered")

# --- BMW-Farben ---
BMW_BLUE = "#1c69d4"
BMW_BLACK = "#000000"
BMW_WHITE = "#ffffff"
BMW_GRAY = "#E5E5E5"
BMW_GREEN = "#3EA83E"

# --- Header mit Logos ---
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    try:
        st.image("bmw_logo.png", width=80)
    except:
        st.empty()
with col2:
    st.markdown(
        f"<h2 style='text-align:center; color:{BMW_BLACK}; margin-top:10px;'>Gefahrstoff-Label-Suche (Logistic Tool)</h2>",
        unsafe_allow_html=True)
with col3:
    try:
        st.image("mini_logo.png", width=120)
    except:
        st.empty()

# --- Untertitel ---
st.markdown(
    "<p style='text-align:center; color:black;'>Classification, Labelling and Packaging of substances and mixtures</p>",
    unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:gray; font-size:14px;'>Verordnung über die Einstufung, Kennzeichnung und Verpackung von Stoffen und Gemischen</p>",
    unsafe_allow_html=True)

st.markdown("---")

# --- Eingabefelder ---
col_input = st.columns([1, 1])
with col_input[0]:
    teilenummer = st.text_input("🔢 Teilenummer", placeholder="Teilenummer eingeben (7 oder 11 Zeichen)")
with col_input[1]:
    land = st.text_input("🌍 Land", placeholder="z. B. DE, Deutschland, FR, etc.")

# --- Startbutton ---
start = st.button("🚀 Start", type="primary")

# --- Statusanzeige ---
status_placeholder = st.empty()

# --- Workflow-Logik ---
if start:
    if not teilenummer or teilenummer.strip() in ["", "Teilenummer eingeben..."] or len(teilenummer.strip()) not in [7, 11]:
        status_placeholder.warning("⚠️ Teilenummer muss genau 7 oder 11 Zeichen lang sein!")
    elif not land or land.strip() in ["", "Land eingeben..."]:
        status_placeholder.warning("⚠️ Bitte ein Land eingeben!")
    else:
        status_placeholder.info("🔍 Workflow läuft...")
        progress = st.progress(0)

        for i in range(100):
            time.sleep(0.02)
            progress.progress(i + 1)
        time.sleep(0.3)

        # Link zur echten Logistic-Tool-Seite
        link = f"https://finalseven.github.io/logistic-tool/?part={teilenummer.strip()}&country={land.strip()}"
        status_placeholder.success(f"✅ Workflow abgeschlossen für {teilenummer.strip()} / {land.strip()}")
        st.markdown(f"<a href='{link}' target='_blank' style='font-size:18px; color:{BMW_BLUE}; text-decoration:none;'>➡️ Zum offiziellen Logistic Tool</a>", unsafe_allow_html=True)

# --- Fußzeile ---
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:gray; font-size:13px;'>© 2025 BMW Group – Logistic Tool App (Webversion)</p>",
    unsafe_allow_html=True)
