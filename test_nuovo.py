import requests

TOKEN = "8968190359:AAEjrT_Aals5ptrCVD4M7CsQM5cLlN-Uez8"
CHAT_ID = "7051807231"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
payload = {
    "chat_id": CHAT_ID,
    "text": "🔥 Bot finalmente attivo e funzionante da Termux!"
}

response = requests.post(url, json=payload)
print("Risposta da Telegram:", response.json())
