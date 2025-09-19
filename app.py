# app.py
import streamlit as st
from load_data import get_dataframes

# =========================
# Config Streamlit
# =========================
st.set_page_config(page_title="HR Dashboard", layout="wide")

# -------------------------
# Auth simple : mot de passe unique (stocké dans st.secrets)
# -------------------------
PASSWORD = st.secrets["auth"]["password"]

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔐 Connexion requise")
    pwd = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if pwd == PASSWORD:
            st.session_state["authenticated"] = True
            st.success("Connexion réussie ✅")
            st.rerun()
        else:
            st.error("Mot de passe incorrect 🚫")
    st.stop()

# Bouton de déconnexion
if st.sidebar.button("Se déconnecter"):
    st.session_state["authenticated"] = False
    st.rerun()

# 🎨 Import police Work Sans (Google Fonts)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Work+Sans:wght@400;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Work Sans', sans-serif;
    }

    h1, h2, h3, h4 {
        font-weight: 600;
        color: #2E86C1;
    }

    .stDataFrame {
        border: 1px solid #ddd;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# Header principal
# =========================
st.markdown("<h1 style='text-align: center;'>HR Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: grey;'>Suivi automatisé des effectifs, entrées/sorties et indicateurs RH</p>", unsafe_allow_html=True)
st.markdown("---")

# Charger les données
arrivees, sorties = get_dataframes()

# Import des KPIs
from kpi1_effectifs import show_kpi1
from kpi2_entrees_sorties import show_kpi2
from kpi3_turnover import show_kpi3
from kpi6_taux_depart import show_kpi6
from kpi7_rupture_pe import show_kpi7

# =========================
# Tabs
# =========================
tabs = st.tabs([
    "👥 Données brutes",
    "📈 Effectifs par contrat /an + pôle/an",
    "📈 Entrées & Sorties / mois/an",
    "📉 Turnover/pôle/an",
    "🚪 Taux de départ CDI par type",
    "⏳ Ancienneté moyenne des CDI par pôle"
])

# Onglet Données brutes
with tabs[0]:
    st.subheader("👥 Données brutes (Google Sheets)")
    with st.expander("📥 Données Arrivées", expanded=True):
        st.dataframe(arrivees, use_container_width=True)
    with st.expander("📤 Données Sorties", expanded=True):
        st.dataframe(sorties, use_container_width=True)

# Onglet KPI1
with tabs[1]:
    st.markdown("## 📈 Effectifs par contrat/an et par pôle / an")
    st.caption("Inclut le stock en fin d'année ainsi que les effectifs moyens pondérés (avec/sans stagiaires).")
    show_kpi1(arrivees)

# Onglet KPI2
with tabs[2]:
    st.markdown("## 📈 Entrées et sorties par mois & par an")
    st.caption("Vue détaillée par mois/année, puis par pôle (hors stagiaires).")
    show_kpi2(arrivees, sorties)

# Onglet KPI3
with tabs[3]:
    st.markdown("## 📉 Turnover par pôle et par an")
    st.caption("Mesure le taux de départs par pôle, en % de l'effectif CDI.")
    show_kpi3(arrivees)

# Onglet KPI6
with tabs[4]:
    st.markdown("## 🚪 Taux de départ CDI par type")
    st.caption("Démissions, fins de contrats, ruptures conventionnelles (initiative employeur).")
    show_kpi6(sorties)

# Onglet KPI7
with tabs[5]:
    st.markdown("## ⏳ Ancienneté moyenne des CDI par pôle")
    show_kpi7(arrivees)
