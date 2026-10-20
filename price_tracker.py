import requests
from bs4 import BeautifulSoup
import time

# --- CONFIGURAZIONE ---
TOKEN = "8968190359:AAEjrT_Aals5ptrCVD4M7CsQM5cllN-Uez"
CHAT_ID = "7051807231"

# Inserisci l'URL del prodotto da monitorare
TARGET_URL = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

# Imposta il prezzo massimo desiderato (Soglia di alert)
TARGET_PRICE = 52.00  

def send_telegram_alert(product_title, current_price, url):
    message = (
        f"🚨 *OFFERTA INTERCETTATA!*\n\n"
        f"📦 *Prodotto:* {product_title}\n"
        f"💰 *Prezzo Attuale:* £{current_price}\n"
        f"🎯 *Soglia Impostata:* £{TARGET_PRICE}\n\n"
        f"🔗 [Vedi Prodotto]({url})"
    )
    
    api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        requests.post(api_url, json=payload)
        print("[+] Alert inviato con successo su Telegram!")
    except Exception as e:
        print(f"[!] Errore nell'invio Telegram: {e}")

def check_price():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        print("[*] Controllo prezzo in corso...")
        response = requests.get(TARGET_URL, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 1. Estrazione Titolo Prodotto
        title = soup.find("h1").text
        
        # 2. Estrazione e pulizia del Prezzo (rimuoviamo i simboli di valuta per convertirlo in numero)
        price_raw = soup.find("p", class_="price_color").text
        # Mantiene solo i numeri e il punto decimale
        clean_price = float(''.join(c for c in price_raw if c.isdigit() or c == '.'))
        
        print(f"[*] Prodotto: {title}")
        print(f"[*] Prezzo Trovato: £{clean_price} (Soglia Target: £{TARGET_PRICE})")
        
        # 3. Logica di Controllo
        if clean_price <= TARGET_PRICE:
            print("[🔥] Il prezzo è sceso sotto la soglia! Invio notifica...")
            send_telegram_alert(title, clean_price, TARGET_URL)
        else:
            print("[i] Prezzo ancora troppo alto. Nessun alert inviato.")

    except Exception as e:
        print(f"[!] Errore durante lo scraping: {e}")

if __name__ == "__main__":
    print("--- MONITOR PREZZI AUTOMATICO AVVIATO ---")
    
    # Esegue il primo controllo all'avvio
    check_price()
