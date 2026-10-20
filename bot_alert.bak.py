from datetime import datetime
import os
import random
import time
from bs4 import BeautifulSoup
from curl_cffi import requests as stealth_requests
import requests

TOKEN = "8968190359:AAF60j6nsjIJztTv9eWjGDVzQ141VpLMK9Q"
CHAT_ID = "7051807231"

DOCS_PATH = os.path.expanduser("~/storage/shared/Documents")
REPORT_FILE = (
    os.path.join(DOCS_PATH, "report.txt")
    if os.path.exists(DOCS_PATH)
    else "report.txt"
)
visti = set()


def scrivi_report(messaggio, tipo="INFO"):
  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  riga = f"[{timestamp}] [{tipo}] {messaggio}\n"
  try:
    with open(REPORT_FILE, "a", encoding="utf-8") as f:
      f.write(riga)
    print(f"[LOG] {riga.strip()}")
  except Exception as e:
    print(f"[!] Errore: {e}")


def send_telegram_message(message):
  url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
  try:
    requests.post(
        url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    )
  except Exception as e:
    scrivi_report(f"Errore Telegram: {e}", "ERRORE")


def check_nike():
  try:
    scrivi_report("Inizio scansione Nike...", "INFO")
    s = stealth_requests.Session(impersonate="chrome120")
    res = s.get(
        "https://www.nike.com/it/w/saldi-sneakers-307gyzv9hdzy7ok", timeout=25
    )
    soup = BeautifulSoup(res.text, "html.parser")
    for item in soup.find_all("div", class_="product-card__body")[:5]:
      t, p, l = (
          item.find("div", class_="product-card__title"),
          item.find("div", class_="product-card__price"),
          item.find("a", class_="product-card__link-overlay"),
      )
      if t and p:
        txt = (
            f"⚡ *SNIPER ALERT: NIKE*\n\n👟 {t.text.strip()}\n💰"
            f" {p.text.strip()}\n🔗 {l['href'] if l else ''}"
        )
        if txt not in visti:
          visti.add(txt)
          send_telegram_message(txt)
  except Exception as e:
    scrivi_report(f"Errore Nike: {e}", "ERRORE")


def check_jd():
  try:
    scrivi_report("Inizio scansione JD Sports (Stealth Completa)...", "INFO")
    sessione_jd = stealth_requests.Session(impersonate="chrome120")
    sessione_jd.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
    })

    sessione_jd.get("https://www.jdsports.it/", timeout=25)
    time.sleep(2)
    res = sessione_jd.get(
        "https://www.jdsports.it/uomo/scarpe-uomo/", timeout=25
    )

    if res.status_code != 200:
      scrivi_report(f"JD HTTP {res.status_code}", "ATTENZIONE")
      return

    soup = BeautifulSoup(res.text, "html.parser")
    items = soup.select(
        "div.itemplp, li.productListItem, div.productCard, div.item, div.card"
    )

    if not items:
      scrivi_report("JD Sports: nessun prodotto trovato.", "ATTENZIONE")
      return

    for item in items[:10]:
      t = item.find(
          ["span", "div", "a", "h4"],
          class_=["itemTitle", "name", "productTitle", "title"],
      )
      p = item.find(
          ["span", "div"], class_=["pri", "price", "salePrice", "nowPrice"]
      )
      l = item.find("a", href=True)

      if t and p:
        titolo = t.text.strip()
        prezzo = p.text.strip()
        link_href = l["href"] if l else ""
        link = (
            f"https://www.jdsports.it{link_href}"
            if link_href.startswith("/")
            else link_href
        )

        txt = (
            f"⚡ *SNIPER ALERT: JD SPORTS*\n\n👟 {titolo}\n💰 {prezzo}\n🔗 {link}"
        )
        if txt not in visti:
          visti.add(txt)
          send_telegram_message(txt)

    scrivi_report("Scansione JD Sports completata.", "INFO")
  except Exception as e:
    scrivi_report(f"Errore JD: {e}", "ERRORE")


def check_zalando():
  try:
    scrivi_report("Inizio scansione Zalando (Stealth)...", "INFO")
    sessione_zalando = stealth_requests.Session(impersonate="chrome120")
    sessione_zalando.get("https://www.zalando.it/", timeout=15)
    time.sleep(2)
    res = sessione_zalando.get(
        "https://www.zalando.it/scarpe-uomo/_saldi/", timeout=25
    )
    soup = BeautifulSoup(res.text, "html.parser")
    for item in soup.find_all("article")[:5]:
      t, l = item.find("h3"), item.find("a")
      if t and l:
        link = (
            l["href"]
            if l["href"].startswith("http")
            else f"https://www.zalando.it{l['href']}"
        )
        txt = (
            f"⚡ *SNIPER ALERT: ZALANDO*\n\n👟 {t.text.strip()}\n🔗"
            f" {link}"
        )
        if txt not in visti:
          visti.add(txt)
          send_telegram_message(txt)
    scrivi_report("Scansione Zalando completata.", "INFO")
  except Exception as e:
    scrivi_report(f"Errore Zalando: {e}", "ERRORE")


if __name__ == "__main__":
  while True:
    scrivi_report("=== Ciclo Sneakers ===", "INFO")
    check_nike()
    time.sleep(5)
    check_jd()
    time.sleep(5)
    check_zalando()
    time.sleep(600)
