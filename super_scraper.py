import requests
from bs4 import BeautifulSoup

def scrape_target_data():
    # URL di esempio (puoi sostituirlo con qualsiasi sito target per i tuoi clienti)
    url = "https://quotes.toscrape.com/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        print("[*] Connessione al target in corso...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        # Analizziamo l'HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Estraiamo i dati desiderati
        results = []
        items = soup.find_all("div", class_="quote")[:5]
        
        for item in items:
            text = item.find("span", class_="text").text
            author = item.find("small", class_="author").text
            results.append(f"• {text} — *{author}*")
            
        return results

    except Exception as e:
        print(f"[!] Errore durante lo scraping: {e}")
        return []

if __name__ == "__main__":
    print("--- AVVIO MOTORE DI RACCOLTA DATI ---")
    data = scrape_target_data()
    for d in data:
        print(d)
