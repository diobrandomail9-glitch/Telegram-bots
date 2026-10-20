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
from concurrent.futures import ThreadPoolExecutor

GREEN = "\033[92m"
DARK_GREEN = "\033[32m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

SFX_LIST = ["ZOT!", "DON!", "BZZT!", "KABOOM!", "TARGET LOCKED!"]
print_lock = threading.Lock()

def matrix_rain_effect():
    print(f"\n{DARK_GREEN}Sincronizzazione con il mainframe della Hunter Association...")
    for _ in range(3):
        linea = "".join(random.choice(["0", "1", " ", "X", "7", "#"]) for _ in range(40))
        print(f"{DARK_GREEN}{linea}{RESET}")
        time.sleep(0.02)
    print(f"{GREEN}[+] Nucleo neurale attivo.{RESET}\n")

def main_banner():
    print(f"{MAGENTA}" + "=" * 65 + f"{RESET}")
    print(f"{GREEN}")
    print("  [+] HUNTER ASSOCIATION: COMMAND FRAMEWORK v10.5 [+]")
    print("  [+] CYBERNETIC RECONNAISSANCE & AUDIT SUITE     [+]")
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
    print(f"{YELLOW}9.{RESET} Disconnessione")
    print(f"{MAGENTA}" + "-" * 65 + f"{RESET}")

def modulo_rileva_rete():
    matrix_rain_effect()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        parti = local_ip.split('.')
        net_prefix = f"{parti[0]}.{parti[1]}.{parti[2]}"
        print(f"{GREEN}[✔] IP Locale rilevato: {local_ip}{RESET}")
        print(f"{GREEN}[✔] Prefisso Consigliato: {net_prefix}{RESET}\n")
    except Exception as e:
        print(f"{RED}[-] Errore: {e}{RESET}\n")

def modulo_discovery():
    prefisso = input(f"{YELLOW}Inserisci prefisso (es. 192.168.162): {RESET}").strip()
    matrix_rain_effect()
    live_hosts = []
    def sonda(ip):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)
        try:
            if s.connect_ex((ip, 80)) == 0 or s.connect_ex((ip, 22)) == 0:
                with print_lock:
                    print(f"{GREEN}[HOST LIVE] -> {ip}{RESET}")
                    live_hosts.append(ip)
        except:
            pass
        finally:
            s.close()
    
    print(f"{CYAN}[!] Scansione sottorete {prefisso}.1-254...{RESET}")
    with ThreadPoolExecutor(max_workers=50) as executor:
        for i in range(1, 255):
            executor.submit(sonda, f"{prefisso}.{i}")
    print(f"\n{GREEN}[✔] Scansione completata. Trovati: {len(live_hosts)}{RESET}\n")

def modulo_portscan():
    target = input(f"{YELLOW}IP target: {RESET}").strip()
    matrix_rain_effect()
    def scansiona(p):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)
        if s.connect_ex((target, p)) == 0:
            with print_lock:
                print(f"{GREEN}[APERTA] Porta {p}{RESET}")
        s.close()
    with ThreadPoolExecutor(max_workers=50) as executor:
        for p in [21, 22, 80, 443, 445, 5555, 8080]:
            executor.submit(scansiona, p)
    print(f"\n{GREEN}[✔] Port scan rapido completato.{RESET}\n")

def modulo_fuzzer():
    url = input(f"{YELLOW}URL target (es. http://127.0.0.1:8080): {RESET}").strip()
    matrix_rain_effect()
    wordlist = ["admin", "login", "dashboard", "config", "api", "backup"]
    def fuzz(w):
        try:
            req = urllib.request.Request(f"{url}/{w}", headers={"User-Agent": "Hunter/10.5"})
            res = urllib.request.urlopen(req, timeout=1.5)
            if res.getcode() == 200:
                with print_lock:
                    print(f"{GREEN}[FOUND 200] -> {url}/{w}{RESET}")
        except:
            pass
    with ThreadPoolExecutor(max_workers=10) as executor:
        for w in wordlist:
            executor.submit(fuzz, w)
    print(f"{GREEN}[✔] Fuzzing completato.{RESET}\n")
def modulo_password_generator():
    matrix_rain_effect()
    caratteri = string.ascii_letters + string.digits + "!@#$%^&*"
    pwd = "".join(random.choice(caratteri) for _ in range(16))
    print(f"{GREEN}[✔] Password Tattica: {CYAN}{pwd}{RESET}\n")

def modulo_banner_grabbing():
    target = input(f"{YELLOW}IP target: {RESET}").strip()
    porta = int(input(f"{YELLOW}Porta: {RESET}"))
    matrix_rain_effect()
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect((target, porta))
        banner = s.recv(1024).decode(errors="ignore").strip()
        print(f"{GREEN}[✔] Banner:\n{banner}{RESET}\n")
        s.close()
    except Exception as e:
        print(f"{RED}[-] Errore: {e}{RESET}\n")

def modulo_dns_resolver():
    prefisso = input(f"{YELLOW}Prefisso (es. 192.168.162): {RESET}").strip()
    matrix_rain_effect()
    def risolvi(ip):
        try:
            h, _, _ = socket.gethostbyaddr(ip)
            with print_lock:
                print(f"{GREEN}[DNS] {ip} -> {h}{RESET}")
        except:
            pass
    with ThreadPoolExecutor(max_workers=30) as executor:
        for i in range(1, 255):
            executor.submit(risolvi, f"{prefisso}.{i}")
    print(f"\n{GREEN}[✔] DNS check completato.{RESET}\n")

def modulo_arp_inspector():
    matrix_rain_effect()
    print(f"{CYAN}[!] Lettura client connessi all'Hotspot...{RESET}\n")
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

def modulo_tcp_interattivo():
    matrix_rain_effect()
    target = input(f"{YELLOW}Inserisci IP target locale: {RESET}").strip()
    try:
        porta = int(input(f"{YELLOW}Inserisci la porta di destinazione (es. 80, 8080, 5555): {RESET}"))
    except ValueError:
        print(f"{RED}[-] Porta non valida.{RESET}\n")
        return
        
    print(f"{CYAN}[!] Tentativo di connessione interattiva verso {target}:{porta}...\n{RESET}")
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(4.0)
        s.connect((target, porta))
        print(f"{GREEN}[✔] Connessione TCP stabilita con successo con {target}:{porta}!{RESET}")
        
        scelta_invio = input(f"{YELLOW}Vuoi inviare una richiesta HTTP di test o un payload custom? (s/n): {RESET}").strip().lower()
        if scelta_invio == 's':
            payload_tipo = input(f"{YELLOW}Scegli tipo payload -> [1] Richiesta HTTP GET standard | [2] Test stringa personalizzata: {RESET}").strip()
            
            if payload_tipo == "1":
                payload = f"GET / HTTP/1.1\r\nHost: {target}\r\nConnection: close\r\n\r\n"
            else:
                payload = input(f"{YELLOW}Inserisci la stringa/comando da inviare: {RESET}") + "\r\n"
                
            s.sendall(payload.encode())
            print(f"{CYAN}[i] Payload inviato. In attesa di risposta dal dispositivo...{RESET}")
            
        risposta = s.recv(2048).decode(errors="ignore")
        if risposta:
            print(f"\n{GREEN}--- RISPOSTA RICEVUTA DAL TARGET ---{RESET}")
            print(f"{CYAN}{risposta}{RESET}")
            print(f"{GREEN}-------------------------------------{RESET}\n")
        else:
            print(f"{YELLOW}[!] Connessione stabilita, ma il target non ha inviato dati spontanei.{RESET}\n")
            
        s.close()
    except Exception as e:
        print(f"{RED}[-] Impossibile comunicare con il target: {e}{RESET}\n")

def main():
    while True:
        main_banner()
        scelta = input(f"{CYAN}HUNTER-CORE> {RESET}").strip()
        if scelta == "0": modulo_rileva_rete()
        elif scelta == "1": modulo_discovery()
        elif scelta == "2": modulo_portscan()
        elif scelta == "3": modulo_fuzzer()
        elif scelta == "4": modulo_password_generator()
        elif scelta == "5": modulo_banner_grabbing()
        elif scelta == "6": modulo_dns_resolver()
        elif scelta == "7": modulo_arp_inspector()
        elif scelta == "8": modulo_tcp_interattivo()
        elif scelta == "9":
            print(f"\n{MAGENTA}Disconnessione. Ciao Hunter!{RESET}\n")
            sys.exit(0)
        else:
            print(f"\n{RED}Comando non valido.{RESET}\n")
        input("Premi [Invio] per continuare...")

if __name__ == "__main__":
    main()

