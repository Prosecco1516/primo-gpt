import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import os

# Autenticazione Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Connessione al foglio di lavoro
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
sheet = client.open_by_key(SHEET_ID).sheet1

# Analisi automatica del topic
def inferisci_topic(message):
    msg = message.lower()
    if "appuntamento" in msg:
        return "appuntamento"
    elif "ferie" in msg:
        return "ferie"
    elif "errore" in msg:
        return "errore"
    elif "documento" in msg:
        return "documento"
    elif "preventivo" in msg:
        return "preventivo"
    elif "cliente" in msg:
        return "cliente"
    elif any(x in msg for x in ["ruota", "bucata", "panne", "fermo"]):
        return "disguido"
    return "altro"

# Funzione di salvataggio
def save_to_sheet(user, message, response, tipo="generico", contesto="non riconosciuto"):
    timestamp = (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")
    topic = inferisci_topic(message)
    sheet.append_row([timestamp, user, message, response, topic, tipo, contesto])
