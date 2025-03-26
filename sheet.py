# sheet.py
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def setup_google_sheet():
    print("🟡 Debug: sono entrato in setup_google_sheet()")

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ]

    filepath = "credentials.json"  # deve stare nella root
    if not os.path.exists(filepath):
        print("❌ File credentials.json NON trovato. Sheets disattivato.")
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
