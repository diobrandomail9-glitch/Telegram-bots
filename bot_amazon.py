from datetime import datetime
import os
import random
import time
from bs4 import BeautifulSoup
import requests

# --- CONFIGURAZIONE BOT PC (Pcscanshopbot) ---
TOKEN = "8704199845:AAH6YVxS8DkqZfxQf2Cr9vtLI6mnR0V6JHg"
CHAT_ID = "7051807231"

# Percorso report in Documenti Android
DOCS_PATH = os.path.expanduser("~/storage/shared/Documents")
if not os.path.exists(DOCS_PATH):
  try:
    os.makedirs(DOCS_PATH, exist_ok=True)
    REPORT_FILE = os.path.join(DOCS_PATH, "report_amazon.txt")
  except:
    REPORT_FILE = "report_amazon.txt"
else:
  REPORT_FILE = os.path.join(DOCS_PATH, "report_amazon.txt")

visti = set()

# Sessione persistente per mantenere i cookie e gestire la navigazione
session = requests.Session()

# Headers avanzati di un browser mobile reale per superare il filtro Cloudflare/Amazon
ADVANCED_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Linux; Android 14; K) AppleWebKit/537.36 (KHTML, like"
        " Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
    ),
    "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Sec-Ch-Ua": (
        '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"'
    ),
    "Sec-Ch-Ua-Mobile": "?1",
    "Sec-Ch-Ua-Platform": '"Android"',
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "Connection": "keep-alive",
}
session.headers.update(ADVANCED_HEADERS)


def scrivi_report(messaggio, tipo="INFO"):
  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  riga = f"[{timestamp}] [{tipo}] {messaggio}\n"
  try:
    with open(REPORT_FILE, "a", encoding="utf-8") as f:
      f.write(riga)
    print(f"[LOG] {riga.strip()}")
  except Exception as e:
    print(f"[!] Errore scrittura report: {e}")


def send_telegram_message(message):
  url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
  payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
  try:
    response = requests.post(url, json=payload, timeout=10)
    res_json = response.json()
    if res_json.get("ok"):
      scrivi_report("Notifica Telegram inviata con successo.", "INFO")
    else:
      scrivi_report(f"Errore API Telegram: {res_json}", "ERRORE")
  except Exception as e:
    scrivi_report(f"Errore di connessione Telegram: {e}", "ERRORE")


def check_amazon_pc():
  home_url = "https://www.amazon.it/"
  target_url = "https://www.amazon.it/s?k=pc+portatile+offerta&i=computers"
  try:
    scrivi_report("Inizio scansione Amazon PC (Modalità Stealth)...", "INFO")

    # Step 1: Warm-up iniziale sulla home di Amazon per ottenere i cookie di sessione legittimi
    session.get(home_url, timeout=15)
    time.sleep(random.uniform(3.0, 5.0))

    # Step 2: Aggiorna il Referer simulando il passaggio interno
    session.headers.update(
        {"Referer": "https://www.amazon.it/", "Sec-Fetch-Site": "same-origin"}
    )
    res = session.get(target_url, timeout=20)

    if res.status_code != 200:
      scrivi_report(
          f"Amazon ha restituito lo status HTTP {res.status_code}", "ATTENZIONE"
      )
      return

    soup = BeautifulSoup(res.text, "html.parser")
    items = soup.find_all("div", {"data-asin": True})

    if not items:
      scrivi_report(
          "Nessun prodotto trovato (blocco anti-bot attivo)", "ATTENZIONE"
      )
      return

    trovati = 0
    for item in items:
      if trovati >= 5:
        break

      link_el = item.find("a", class_="a-link-normal")
      title_el = item.find("h2") or item.find("span", class_="a-size-base-plus")
      price_el = item.find("span", class_="a-price-whole")

      if title_el and price_el and link_el:
        titolo = title_el.text.strip()
        prezzo = f"€{price_el.text.strip()}"
        href = link_el.get("href", "")

        if href.startswith("/"):
          link = f"https://www.amazon.it{href}"
        else:
          link = href

        if "/ref=" in link:
          link = link.split("/ref=")[0]

        dettagli = (
            f"💻 *SNIPER ALERT: PC IN OFFERTA*\n\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🖥️ *Modello:* {titolo}\n"
            f"🏪 *Negozio:* Amazon Italia\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"💰 *Prezzo:* {prezzo}\n\n"
            f"🔗 [ACQUISTA SUBITO]({link})\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        )

        if dettagli not in visti:
          visti.add(dettagli)
          send_telegram_message(dettagli)
          trovati += 1

    scrivi_report(
        f"Scansione Amazon completata. Prodotti analizzati: {trovati}", "INFO"
    )

  except requests.exceptions.Timeout:
    scrivi_report("Timeout durante la connessione ad Amazon.", "TIMEOUT")
  except Exception as e:
    scrivi_report(
        f"Errore critico durante lo scraping di Amazon: {str(e)}", "CRITICAL"
    )


def job():
  scrivi_report("=== Inizio nuovo ciclo di controllo PC Amazon ===", "INFO")
  check_amazon_pc()


if __name__ == "__main__":
  scrivi_report("DataFalco Amazon PC Bot (Anti-Detection) avviato.", "INFO")
  while True:
    try:
      job()
    except Exception as e:
      scrivi_report(
          f"Errore imprevisto nel ciclo principale: {e}", "CRITICAL"
      )

    scrivi_report("Attesa di 15 minuti per il prossimo controllo...", "INFO")
    time.sleep(900)
