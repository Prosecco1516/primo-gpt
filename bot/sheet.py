# sheet.py
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def setup_google_sheet():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ]

    filepath = filepath = "/etc/secrets/credentials.json"

    if not os.path.exists(filepath):
        print("❌ File credentials.json NON trovato nella root del progetto.")
        print("📂 File presenti:", os.listdir("."))
        return False, None

    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name(filepath, scope)
        client = gspread.authorize(creds)
        sheet = client.open_by_key("109018550274954569288").sheet1
        print("✅ Google Sheets attivo")
        return True, sheet
    except Exception as e:
        print(f"❌ Errore durante la connessione a Google Sheets: {e}")
        return False, None
