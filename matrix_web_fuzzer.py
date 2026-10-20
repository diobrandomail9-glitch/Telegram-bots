import urllib.request
import urllib.error
import sys
import time
import threading
import random
import json
from concurrent.futures import ThreadPoolExecutor

# Colori Matrix & Cyberpunk
GREEN = "\033[92m"
DARK_GREEN = "\033[32m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

print_lock = threading.Lock()

def banner_fuzzer():
    print(f"{MAGENTA}" + "=" * 60 + f"{RESET}")
    print(f"{GREEN}")
    print("  [+] H U N T E R   W E B   F U Z Z E R   [+]")
    print("  [+] SKILL 4: HIDDEN ENDPOINT DISCOVERY  [+]")
    print(f"{RESET}")
    print(f"{MAGENTA}" + "=" * 60 + f"{RESET}")

def test_endpoint(url_base, path, risultati_trovati):
    url = f"{url_base}/{path.strip('/')}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "HunterAssociationFuzzer/4.0"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=2.0) as response:
            code = response.getcode()
            if code == 200:
                msg = f"{GREEN}[FOUND - 200 OK] -> {url}{RESET}"
                with print_lock:
                    print(msg)
                    risultati_trovati.append({"path": url, "status": 200})
    except urllib.error.HTTPError as e:
        # Anche un 403 Forbidden o 401 Unauthorized indicano che la cartella esiste!
        if e.code in [401, 403, 405]:
            msg = f"{YELLOW}[PROTECTED - {e.code}] -> {url}{RESET}"
            with print_lock:
                print(msg)
                risultati_trovati.append({"path": url, "status": e.code})
    except Exception:
        pass

def main():
    banner_fuzzer()
    
    target_url = input(f"{YELLOW}Inserisci l'URL target (es. http://192.168.1.10:8080): {RESET}").strip()
    if not target_url.startswith("http"):
        print(f"{RED}[-] Errore: L'URL deve iniziare con http:// o https://{RESET}")
        sys.exit(1)

    # Wordlist incorporata di endpoint comuni da cacciare
    wordlist = [
        "admin", "login", "dashboard", "config", "api", "backup", 
        "secret", "test", "server-status", "index.php", "wp-login.php",
        "db", "database", "users", "uploads", "private", "robots.txt",
        "assets", "js", "css", "portal", "gateway", "v1", "v2"
    ]

    print(f"\n{CYAN}[!] Caricamento wordlist tattica ({len(wordlist)} parole chiave)...{RESET}")
    print(f"{CYAN}[!] Avvio fuzzer ad alta velocità su {target_url}...{RESET}\n")
    
    trovati = []
    inizio = time.time()

    with ThreadPoolExecutor(max_workers=20) as executor:
        for word in wordlist:
            executor.submit(test_endpoint, target_url, word, trovati)

    fine = time.time()

    # Salvataggio report
    report_name = "hunter_web_fuzz_report.json"
    with open(report_name, "w") as f:
        json.dump(trovati, f, indent=4)

    print(f"\n{GREEN}[✔] Fuzzing completato in {fine - inizio:.2f} secondi!{RESET}")
    print(f"{MAGENTA}[i] Endpoint validi scoperti: {len(trovati)}{RESET}")
    print(f"{MAGENTA}[i] Report salvato in: {report_name}{RESET}\n")

if __name__ == "__main__":
    main()
