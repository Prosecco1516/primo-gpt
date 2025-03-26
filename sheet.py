import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime


# Autenticazione e connessione allo Sheet
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope
)

gs_client = gspread.authorize(creds)
sheet = gs_client.open("PrimoGPT").sheet1  # Assicurati che il nome sia corretto


def salva_istruzione_su_sheet(utente, messaggio, risposta):
    try:
        if not messaggio.lower().startswith("istruzione:"):
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nuova_riga = [timestamp, utente, messaggio, risposta]
        sheet.append_row(nuova_riga)

    except Exception as e:
        print("Errore nel salvataggio su Google Sheet:", e)
