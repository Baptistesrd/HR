import os
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

load_dotenv()
print("DEBUG .env →", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))


def get_dataframes():
    # Connexion
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"), scope)
    client = gspread.authorize(creds)

    sheet_key = os.getenv("GSHEET_KEY")
    spreadsheet = client.open_by_key(sheet_key)

    # Charger les deux onglets
    arrivees = pd.DataFrame(spreadsheet.worksheet(os.getenv("SHEET_ARRIVEES")).get_all_records())
    sorties = pd.DataFrame(spreadsheet.worksheet(os.getenv("SHEET_SORTIES")).get_all_records())

    # Conversion des colonnes date
    for col in ["Date d'arrivée", "Date de fin (si applicable)"]:
        if col in arrivees.columns:
            arrivees[col] = pd.to_datetime(arrivees[col], errors="coerce", dayfirst=True)

    for col in ["Date d'arrivée", "Date de départ prévue", "Date d'information du départ"]:
        if col in sorties.columns:
            sorties[col] = pd.to_datetime(sorties[col], errors="coerce", dayfirst=True)

    return arrivees, sorties
