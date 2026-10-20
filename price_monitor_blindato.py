import requests
from bs4 import BeautifulSoup
import time
import random

# --- CONFIGURAZIONE ---
TOKEN = "8968190359:AAEjrT_Aals5ptrCVD4M7CsQM5cllN-Uez"
CHAT_ID = "7051807231"

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

CHECK_INTERVAL = 3600  # Intervallo tra i cicli completi (in secondi)

# Lista di User-Agent reali per la rotazione (Anti-Block)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
]

def send_telegram_alert(product_title, current_price, target_price, url):
    message = (
        f"🛡️ *ALERT PREZZO BLINDATO!*\n\n"
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
        requests.post(api_url, json=payload, timeout=10)
        print(f"[+] Notifica Telegram inviata per: {product_title}")
    except Exception as e:
        print(f"[!] Errore invio Telegram: {e}")

def check_prices():
    print("\n[*] Avvio scansione blindata dei prodotti...")
    
    for item in PRODUCTS_TO_WATCH:
        url = item["url"]
        target_price = item["target_price"]
        
        # Seleziona casualmente uno User-Agent per ogni richiesta
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        
        try:
            # Timeout di sicurezza per evitare blocchi infiniti se il sito è lento
            response = requests.get(url, headers=headers, timeout=15)
            
            # Se il sito blocca la richiesta (es. errore 403 o 503)
            if response.status_code != 200:
                print(f" [!] Attenzione: Il sito ha risposto con codice {response.status_code} per {url}")
                continue
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            title = soup.find("h1").text.strip()
            price_raw = soup.find("p", class_="price_color").text
            clean_price = float(''.join(c for c in price_raw if c.isdigit() or c == '.'))
            
            print(f" - {title}: £{clean_price} (Target: £{target_price})")
            
            if clean_price <= target_price:
                print(f"   [🔥] TARGET RAGGIUNTO! Invio alert...")
                send_telegram_alert(title, clean_price, target_price, url)
                
        except requests.exceptions.Timeout:
            print(f" [!] Timeout nella connessione a {url}. Riproverò al prossimo ciclo.")
        except Exception as e:
            print(f" [!] Errore imprevisto sul prodotto: {e}")
        
        # Pausa casuale tra una richiesta e l'altra (da 3 a 7 secondi) per massima discrezione
        time.sleep(random.uniform(3, 7))

if __name__ == "__main__":
    print("--- SISTEMA DI MONITORAGGIO BLINDATO H24 ATTIVO ---")
    
    while True:
        check_prices()
        # Aggiunge un piccolo jitter anche alla pausa principale
        sleep_time = CHECK_INTERVAL + random.randint(-300, 300)
        print(f"[*] Ciclo terminato. Prossimo controllo tra circa {int(sleep_time/60)} minuti...\n")
        time.sleep(sleep_time)
