import requests
from bs4 import BeautifulSoup
import time

TOKEN = "8968190359:AAEjrT_Aals5ptrCVD4M7CsQM5cLlN-Uez8"
CHAT_ID = "7051807231"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print(f"[!] Errore invio Telegram: {e}")

def job():
    print("[*] Scansione target in corso...")
    url = "https://quotes.toscrape.com/"
    
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Prende la prima citazione del giorno come esempio di monitoraggio
        quote_div = soup.find("div", class_="quote")
        quote = quote_div.find("span", class_="text").text
        author = quote_div.find("small", class_="author").text
        
        message = f"🚨 *AGGIORNAMENTO TARGET RILEVATO!*\n\n{quote}\n\nAutore: _{author}_"
        send_telegram_message(message)
        print("[+] Notifica inviata con successo!")
        
    except Exception as e:
        print(f"[!] Errore nello scraping: {e}")

if __name__ == "__main__":
    print("--- AGENTE AUTOMATICO AVVIATO SU TERMUX ---")
    print("Il bot è in ascolto. Premi Ctrl+C per interrompere.")
    
    while True:
        job()
        # Imposta l'intervallo di attesa (es. ogni 60 secondi per i test, o 3600 per 1 ora)
        print("[*] In pausa in attesa del prossimo ciclo...")
        time.sleep(60)
