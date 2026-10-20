import requests
from bs4 import BeautifulSoup
import time

# --- CONFIGURAZIONE ---
TOKEN = "8968190359:AAEjrT_Aals5ptrCVD4M7CsQM5cllN-Uez"
CHAT_ID = "7051807231"

# Lista dei prodotti da monitorare (URL + Prezzo massimo desiderato)
PRODUCTS_TO_WATCH = [
    {
        "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html",
        "target_price": 52.00
    },
    {
        "url": "https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html",
        "target_price": 55.00
    }
]

# Intervallo di controllo in secondi (es. 3600 = 1 ora)
CHECK_INTERVAL = 3600  

def send_telegram_alert(product_title, current_price, target_price, url):
    message = (
        f"🚨 *OFFERTA MULTIPLA INTERCETTATA!*\n\n"
        f"📦 *Prodotto:* {product_title}\n"
        f"💰 *Prezzo Attuale:* £{current_price}\n"
        f"🎯 *Tua Soglia:* £{target_price}\n\n"
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
        print(f"[+] Alert inviato per: {product_title}")
    except Exception as e:
        print(f"[!] Errore invio Telegram: {e}")

def check_prices():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    print("\n[*] Inizio scansione della lista prodotti...")
    for item in PRODUCTS_TO_WATCH:
        url = item["url"]
        target_price = item["target_price"]
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            title = soup.find("h1").text
            price_raw = soup.find("p", class_="price_color").text
            clean_price = float(''.join(c for c in price_raw if c.isdigit() or c == '.'))
            
            print(f" - {title}: £{clean_price} (Target: £{target_price})")
            
            if clean_price <= target_price:
                print(f"   [🔥] PREZZO TARGET RAGGIUNTO per {title}!")
                send_telegram_alert(title, clean_price, target_price, url)
                
        except Exception as e:
            print(f" [!] Errore sul prodotto {url}: {e}")
        
        # Breve pausa tra una richiesta e l'altra per non sovraccaricare il server target
        time.sleep(2)

if __name__ == "__main__":
    print("--- MONITORAGGIO MULTIPLO H24 AVVIATO ---")
    
    while True:
        check_prices()
        print(f"[*] Ciclo completato. Pausa di {CHECK_INTERVAL} secondi...\n")
        time.sleep(CHECK_INTERVAL)
