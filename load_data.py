# load_data.py
import streamlit as st
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

def get_dataframes():
    # Connexion via st.secrets (pas de fichier local)
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    creds_dict = dict(st.secrets["gcp"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
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
