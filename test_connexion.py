import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv

load_dotenv()

# Charger les identifiants
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"), scope)
client = gspread.authorize(creds)

# Ouvrir le fichier
sheet_key = os.getenv("GSHEET_KEY")
spreadsheet = client.open_by_key(sheet_key)

# Tester accès aux deux onglets
arrivees = spreadsheet.worksheet(os.getenv("SHEET_ARRIVEES"))
sorties = spreadsheet.worksheet(os.getenv("SHEET_SORTIES"))

print("✅ Connexion réussie !")
print("Nombre d'arrivées :", len(arrivees.get_all_records()))
print("Nombre de sorties :", len(sorties.get_all_records()))
