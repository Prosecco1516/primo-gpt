# sheet.py
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os
from telegram import Update
from telegram.ext import ContextTypes

# Autenticazione con Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Apri il foglio di lavoro tramite ID
SHEET_ID = os.getenv("GOOGLE_SHEET_ID")
sheet = client.open_by_key(SHEET_ID).sheet1

def save_to_sheet(user, message, response):
    if not message.lower().startswith("istruzione:"):
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([timestamp, user, message, response])

# Handler da integrare in handlers.py
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.full_name
    message = update.message.text
    response = f"Hai scritto: {message}"

    await update.message.reply_text(response)
    save_to_sheet(user, message, response)

