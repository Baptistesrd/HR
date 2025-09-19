# load_data.py
import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials


def get_dataframes():
    # Scopes requis pour Google Sheets + Drive
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    # Connexion via st.secrets (pas de fichier local)
    creds = Credentials.from_service_account_info(
        dict(st.secrets["gcp"]), scopes=scopes
    )
    client = gspread.authorize(creds)

    # Récupérer paramètres depuis secrets
    sheet_key = st.secrets["gcp"]["GSHEET_KEY"]
    sheet_arrivees = st.secrets["gcp"]["SHEET_ARRIVEES"]
    sheet_sorties = st.secrets["gcp"]["SHEET_SORTIES"]

    spreadsheet = client.open_by_key(sheet_key)

    # Charger les deux onglets
    arrivees = pd.DataFrame(spreadsheet.worksheet(sheet_arrivees).get_all_records())
    sorties = pd.DataFrame(spreadsheet.worksheet(sheet_sorties).get_all_records())

    # Conversion des colonnes de dates
    for col in ["Date d'arrivée", "Date de fin (si applicable)"]:
        if col in arrivees.columns:
            arrivees[col] = pd.to_datetime(arrivees[col], errors="coerce", dayfirst=True)

    for col in ["Date d'arrivée", "Date de départ prévue", "Date d'information du départ"]:
        if col in sorties.columns:
            sorties[col] = pd.to_datetime(sorties[col], errors="coerce", dayfirst=True)

    return arrivees, sorties
