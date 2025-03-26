# sheet.py
import gspread
from datetime import datetime
import os
from oauth2client.service_account import ServiceAccountCredentials

def salva_istruzione(mittente, testo, risposta):
    if not testo.lower().startswith("istruzione:"):
        return  # Ignora tutto ciò che non è istruzione

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(os.getenv("SHEET_ID")).sheet1
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([timestamp, mittente, testo, risposta])
