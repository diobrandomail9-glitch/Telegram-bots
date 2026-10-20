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
EOF

nohup python bot_scraper_definitivo.py &
cat << 'EOF' > price_tracker.py
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
EOF

python price_tracker.py
nohup python price_tracker.py &
cat << 'EOF' > price_monitor_h24.py
import requests
from bs4 import BeautifulSoup
import time

# --- CONFIGURAZIONE ---
TOKEN = "8968190359:AAEjrT_Aals5ptrCVD4M7CsQM5cllN-Uez"
CHAT_ID = "7051807231"

TARGET_URL = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
TARGET_PRICE = 52.00  

# Intervallo di controllo in secondi (es. 3600 = 1 ora, 300 = 5 minuti)
CHECK_INTERVAL = 3600  

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
        
        title = soup.find("h1").text
        price_raw = soup.find("p", class_="price_color").text
        clean_price = float(''.join(c for c in price_raw if c.isdigit() or c == '.'))
        
        print(f"[*] Prodotto: {title} | Prezzo Trovato: £{clean_price} (Target: £{TARGET_PRICE})")
        
        if clean_price <= TARGET_PRICE:
            print("[🔥] Il prezzo è sceso sotto la soglia! Invio notifica...")
            send_telegram_alert(title, clean_price, TARGET_URL)
        else:
            print("[i] Prezzo ancora alto. Nessun alert inviato.")

    except Exception as e:
        print(f"[!] Errore durante lo scraping: {e}")

if __name__ == "__main__":
    print("--- MONITORAGGIO CONTINUO AVVIATO ---")
    
    while True:
        check_price()
        print(f"[*] In pausa per {CHECK_INTERVAL} secondi...\n")
        time.sleep(CHECK_INTERVAL)
EOF

nohup python price_monitor_h24.py &
cat << 'EOF' > multi_price_monitor.py
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
EOF

nohup python multi_price_monitor.py &
pgrep -f python
cat << 'EOF' > price_monitor_blindato.py
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
EOF

pkill -f python
nohup python price_monitor_blindato.py &
ps aux | grep python
python bot_alert.py
nano bot_alert.py
python bot_alert.py
curl -s -X POST "https://api.telegram.org/bot8968190359:AAEjrT_Aals5ptrCVD4M7CSqM5cl1N-Uez/sendMessage" -d "chat_id=7051807231" -d "text=Test"
nano bot_alert.py
python bot_alert.py
nano bot_alert.py
python -c "import requests; print(requests.post('https://api.telegram.org/bot8968190359:AAEjrT_Aals5ptrCVD4M7CsQM5cL1N-Uez8/sendMessage', json={'chat_id': '7051807231', 'text': 'Test finale'}).json())"
nano bot_alert.py
python bot_alert.py
nano bot_alert.py
python bot_alert.py
termux-setup-storage
nano bot_alert.py
nohup python bot_alert.py &
ls -la ~/storage/shared/Documents/report.txt
nano bot_alert.py
nohup python bot_alert.py &
nano bot_amazon.py
nohup python bot_amazon.py &
nano bot_amazon.py
nohup python bot_amazon.py &
nano bot_amazon.py
nohup python bot_amazon.py &
pkill -f python
nohup python bot_alert.py &
nohup python bot_amazon.py &
pkill -f bot_amazon.py
nano bot_amazon.py
nohup python bot_amazon.py &
nano bot_alert.py
pkill -f python
nohup python bot_alert.py &
nohup python bot_amazon.py &
nano bot_alert.py
pkill -f python
nohup python bot_alert.py &
nohup python bot_amazon.py &
nano bot_alert.py
pkill -f python
nohup python bot_alert.py &
nohup python bot_amazon.py &
nano bot_alert.py
pkill -f python
nohup python bot_alert.py &
nohup python bot_amazon.py &
nano bot_alert.py
Nano bot_amazon.py
nano bot_amazon.py
pkill -f python
nohup python bot_alert.py &
nohup python bot_amazon.py &
nano bot_amazon.py
pkill -f python
nohup python bot_amazon.py &
nohup python bot_alert.py &
pip install curl_cffi
nano bot_alert.py
pkill -f python; nohup python bot_alert.py & nohup python bot_amazon.py &
nano bot_alert.py
cat ~/storage/shared/Documents/report.txt
nano bot_alert.py
pkill -9 -f python
nohup python bot_alert.py &
nohup python bot_amazon.py &
tail -f ~/storage/shared/Documents/report.txt
pkill -9 -f python
rm bot_alert.py
nano bot_alert.py
nohup python bot_alert.py &
nohup python bot_amazon.py &
tail -f ~/storage/shared/Documents/report.txt
pkill -9 -f python
rm bot_alert.py
nano bot_alert.py
pkill -9 -f python
nohup python bot_alert.py &
nohup python bot_amazon.py &
tail -f ~/storage/shared/Documents/report.txt
pkill -9 -f python
rm bot_alert.py
nano bot_alert.py
nohup python bot_alert.py &
nohup python bot_amazon.py &
tail -f ~/storage/shared/Documents/report.txt
pkill -9 -f python
rm bot_alert.py
nano bot_alert.py
nohup python bot_alert.py &
nohup python bot_amazon.py &
tail -f ~/storage/shared/Documents/report.txt
pkill -9 -f python
rm bot_alert.py
nano bot_alert.py
nohup python bot_alert.py &
nohup python bot_amazon.py &
tail -f ~/storage/shared/Documents/report.txt
pkill -9 -f python
nano bot_alert.py
cm bot_alert.py
cp bot_alert.py bot_alert.bak.py
rm bot_alert.py
nano bot_alert.py
cp bot_alert.py bot_alert.bak.py
sed -i 's|^TOKEN *=.*|TOKEN = "8968190359:AAF0CRiIWfqxcXm0ZORSLS6eNpUP2L4iy1k"|' bot_alert.py
sed -i 's|^CHAT_ID *=.*|CHAT_ID = "7051807231"|' bot_alert.py
echo "---- controllo ----"
grep -nE '^(TOKEN|CHAT_ID) *=' bot_alert.py
pip install python-telegram-bot requests beautifulsoup4
nano bot_alert.py
nohup python bot_alert.py &
nohup python bot_amazon.py &
tail -f ~/storage/shared/Documents/report.txt
nano bot_alert.py
rm bot_alert.py
nano bot_alert.py
nohup python bot_alert.py &
nohup python bot_amazon.py &
tail -f ~/storage/shared/Documents/report.txt
pkill -9 -f python
rm bot_alert.py
nano bot_alert.py
nohup python bot_alert.py &
nohup python bot_amazon.py &
tail -f ~/storage/shared/Documents/report.txt
termux-setup-storage
pkg update && pkg upgrade -y
pkg install x11-repo proot-distro pulseaudio -y
# Installa Debian nel terminale
proot-distro install debian
# Entra dentro Debian per configurare la grafica
proot-distro login debian
pulseaudio --start --exit-idle-time=-1
termux-x11 :1 -xstartup "proot-distro login debian -- shared-tmp --env DISPLAY=:1 startxfce4" &
exit)
curl -L -o /sdcard/Download/termux-x11.apk https://github.com
