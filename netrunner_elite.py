import socket
import sys
import time
import threading
import random
import json
from concurrent.futures import ThreadPoolExecutor

# Colori ANSI Neon
CYAN = "\033[96m"
GREEN = "\033[92m"
MAGENTA = "\033[95m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

SFX_LIST = ["ZOT!", "DON!", "BZZT!", "KABOOM!", "CRASH!", "EXPLOIT!"]
print_lock = threading.Lock()

def banner_elite():
    print(f"{MAGENTA}" + "=" * 60 + f"{RESET}")
    print(f"{CYAN}")
    print(r"  _   _ _____ _____ ____  _   _ _   _ _   _ _____ ____  ")
    print(r" | \ | | ____|_   _|  _ \| | | | \ | | \ | | ____|  _ \ ")
    print(r" |  \| |  _|   | | | |_) | | | |  \| |  \| |  _| | |_) |")
    print(r" | |\  | |___  | | |  _ <| |_| | |\  | |\  | |___|  _ < ")
    print(r" |_| \_|_____| |_| |_| \_\\___/|_| \_|_| \_|_____|_| \_\ ")
    print(f"{RESET}")
    print(f"{MAGENTA}       [ NETRUNNER ELITE SUITE v5.0 - DEEP RECON ]{RESET}")
    print(f"{MAGENTA}" + "=" * 60 + f"{RESET}")
    print(f"{YELLOW}1.{RESET} Scansione Mirata + HTTP Fingerprinting & Headers")
    print(f"{YELLOW}2.{RESET} Network Sweep Massivo (Sottorete Locale)")
    print(f"{YELLOW}3.{RESET} Esci dal Terminale")
    print(f"{MAGENTA}" + "-" * 60 + f"{RESET}")

def analizza_http_e_banner(target_ip, porta):
    """Esegue un banner grabbing avanzato o un'interrogazione HTTP se è una porta web"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.5)
    info_dettaglio = "Servizio attivo (Nessun banner)"
    try:
        s.connect((target_ip, porta))
        
        # Se la porta è tipicamente web, mandiamo una richiesta HTTP GET
        if porta in [80, 443, 8080, 8443, 5000, 3000]:
            request = f"GET / HTTP/1.1\r\nHost: {target_ip}\r\nUser-Agent: NetrunnerElite/5.0\r\nConnection: close\r\n\r\n"
            s.sendall(request.encode())
        
        risposta = s.recv(2048).decode(errors="ignore").strip()
        if risposta:
            # Preleviamo la prima linea o informazioni utili
            prime_linee = risposta.split("\n")[0]
            info_dettaglio = f"Headers/Banner -> {prime_linee}"
    except Exception:
        pass
    finally:
        s.close()
    return info_dettaglio

def scansiona_porta(target_ip, porta, risultati_lista):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.4)
    try:
        if s.connect_ex((target_ip, porta)) == 0:
            sfx = random.choice(SFX_LIST)
            dettaglio_servizio = analizza_http_e_banner(target_ip, porta)
            
            msg = f"{GREEN}[{sfx}] {target_ip}:{porta} -> APERTA | {dettaglio_servizio}{RESET}"
            
            # Struttura dati per il report JSON
            risultato_dict = {
                "ip": target_ip,
                "port": porta,
                "status": "OPEN",
                "service_info": dettaglio_servizio
            }
            
            with print_lock:
                print(msg)
                risultati_lista.append(risultato_dict)
    except socket.error:
        pass
    finally:
        s.close()

def ping_host(base_ip, host_num, risultati_lista):
    target_ip = f"{base_ip}.{host_num}"
    common_ports = [21, 22, 80, 443, 3000, 8080, 8443]
    for porta in common_ports:
        scansiona_porta(target_ip, porta, risultati_lista)

def main():
    while True:
        banner_elite()
        scelta = input(f"{CYAN}Seleziona opzione [1-3]: {RESET}").strip()

        if scelta == "1":
            target_ip = input(f"{YELLOW}Inserisci IP target (es. 127.0.0.1): {RESET}").strip()
            try:
                start_p = int(input(f"{YELLOW}Porta di inizio: {RESET}"))
                end_p = int(input(f"{YELLOW}Porta di fine: {RESET}"))
            except ValueError:
                print(f"{RED}[-] Errore: Inserisci numeri validi!{RESET}\n")
                continue

            risultati = []
            print(f"\n{CYAN}[!] Avvio ricognizione profonda su {target_ip} ({start_p}-{end_p})...{RESET}")
            inizio = time.time()

            with ThreadPoolExecutor(max_workers=100) as executor:
                for porta in range(start_p, end_p + 1):
                    executor.submit(scansiona_porta, target_ip, porta, risultati)

            fine = time.time()
            
            # Salvataggio in formato JSON professionale
            json_filename = f"report_elite_{target_ip.replace('.', '_')}.json"
            with open(json_filename, "w") as jf:
                json.dump(risultati, jf, indent=4)

            print(f"\n{GREEN}[✔] Operazione completata in {fine - inizio:.2f} secondi!{RESET}")
            print(f"{MAGENTA}[i] Report strutturato salvato in: {json_filename}{RESET}\n")
            input("Premi [Invio] per tornare al menu...")

        elif scelta == "2":
            prefisso = input(f"{YELLOW}Inserisci i primi 3 numeri della rete (es. 192.168.1): {RESET}").strip()
            risultati = []
            
            print(f"\n{CYAN}[!] Sweep massivo della sottorete {prefisso}.1-254 in corso...{RESET}")
            inizio = time.time()

            with ThreadPoolExecutor(max_workers=50) as executor:
                for host in range(1, 255):
                    executor.submit(ping_host, prefisso, host, risultati)

            fine = time.time()
            
            json_filename = "report_network_elite.json"
            with open(json_filename, "w") as jf:
                json.dump(risultati, jf, indent=4)

            print(f"\n{GREEN}[✔] Network sweep completato in {fine - inizio:.2f} secondi!{RESET}")
            print(f"{MAGENTA}[i] Report JSON salvato in: {json_filename}{RESET}\n")
            input("Premi [Invio] per tornare al menu...")

        elif scelta == "3":
            print(f"\n{MAGENTA}Disconnessione dalla rete quantistica. A presto, Netrunner.{RESET}\n")
            sys.exit(0)
        else:
            print(f"\n{RED}[-] Comando non valido.{RESET}\n")

if __name__ == "__main__":
    main()
