import socket
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

SFX_LIST = ["TARGET LOCKED!", "HOST DETECTED!", "NODE FOUND!", "BREACH!"]
print_lock = threading.Lock()

def matrix_rain_effect():
    print(f"\n{DARK_GREEN}Inizializzazione scansione radar nella sottorete...")
    for _ in range(6):
        linea = "".join(random.choice(["0", "1", " ", "X", "7", "#"]) for _ in range(45))
        print(f"{DARK_GREEN}{linea}{RESET}")
        time.sleep(0.04)
    print(f"{GREEN}[+] Radar attivo. Scansione frequenze in corso...{RESET}\n")

def banner_hunter():
    print(f"{MAGENTA}" + "=" * 60 + f"{RESET}")
    print(f"{GREEN}")
    print("  [+] H U N T E R   A S S O C I A T I O N [+]")
    print("  [+] ACTIVE HOST DISCOVERY MODULE v3.0   [+]")
    print(f"{RESET}")
    print(f"{MAGENTA}" + "=" * 60 + f"{RESET}")

def sonda_host(ip, porte_campione, live_hosts_lista):
    host_vivo = False
    porte_aperte_trovate = []

    for porta in porte_campione:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)
        try:
            if s.connect_ex((ip, porta)) == 0:
                host_vivo = True
                porte_aperte_trovate.append(porta)
        except socket.error:
            pass
        finally:
            s.close()
        
        if host_vivo and len(porte_aperte_trovate) >= 2:
            break

    if host_vivo:
        sfx = random.choice(SFX_LIST)
        msg = f"{GREEN}[{sfx}] Host Attivo Trovato -> {ip} | Porte: {porte_aperte_trovate}{RESET}"
        
        item = {
            "host": ip,
            "status": "ALIVE",
            "open_probes": porte_aperte_trovate
        }
        
        with print_lock:
            print(msg)
            live_hosts_lista.append(item)

def main():
    banner_hunter()
    prefisso = input(f"{YELLOW}Inserisci i primi 3 blocchi della rete (es. 192.168.1): {RESET}").strip()
    
    if not prefisso:
        print(f"{RED}[-] Inserisci un prefisso di rete valido.{RESET}")
        sys.exit(1)

    porte_campione = [22, 80, 135, 445, 8080, 62078]
    
    matrix_rain_effect()
    live_hosts = []
    inizio = time.time()

    print(f"{CYAN}[!] Sonda aggressiva avviata su {prefisso}.1 fino a {prefisso}.254...{RESET}\n")

    with ThreadPoolExecutor(max_workers=100) as executor:
        for host_num in range(1, 255):
            ip_target = f"{prefisso}.{host_num}"
            executor.submit(sonda_host, ip_target, porte_campione, live_hosts)

    fine = time.time()

    report_name = f"hunter_discovery_{prefisso.replace('.', '_')}.json"
    with open(report_name, "w") as f:
        json.dump(live_hosts, f, indent=4)

    print(f"\n{GREEN}[✔] Sweep di scoperta completato in {fine - inizio:.2f} secondi!{RESET}")
    print(f"{MAGENTA}[i] Totale host attivi individuati: {len(live_hosts)}{RESET}")
    print(f"{MAGENTA}[i] Report tattico salvato in: {report_name}{RESET}\n")

if __name__ == "__main__":
    main()
