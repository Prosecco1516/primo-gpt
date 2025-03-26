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

    if os.path.exists("credentials.json"):
        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
            client = gspread.authorize(creds)
            sheet = client.open_by_key("109018550274954569288").sheet1
            print("✅ Google Sheets attivo")
            return True, sheet
        except Exception as e:
            print(f"⚠️ Errore nell'accesso a Google Sheets: {e}")
            return False, None
    else:
        print("⚠️ File credentials.json non trovato. Sheets disattivato.")
        return False, None
