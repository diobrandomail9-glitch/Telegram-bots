import requests
from bs4 import BeautifulSoup

TOKEN = "8968190359:AAEjrT_Aals5ptrCVD4M7CsQM5cllN-Uez"
CHAT_ID = "7051807231"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

def job():
    url = "https://quotes.toscrape.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    quote = soup.find("span", class_="text").text
    author = soup.find("small", class_="author").text
    
    message = f"🚨 *NUOVO DATO INTERCETTATO!*\n\n{quote}\n\nAutore: _{author}_"
    send_telegram_message(message)
    print("[+] Notifica inviata con successo via Telegram!")

if __name__ == "__main__":
    job()
