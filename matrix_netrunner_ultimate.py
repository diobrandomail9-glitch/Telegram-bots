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

SFX_LIST = ["ZOT!", "DON!", "BZZT!", "KABOOM!", "CRASH!", "EXPLOIT!"]
print_lock = threading.Lock()

def matrix_rain_effect():
    """Simula una breve pioggia di codice in stile Matrix"""
    print(f"\n{DARK_GREEN}Infiltrazione nella Matrix in corso...")
    for _ in range(8):
        linea = "".join(random.choice(["0", "1", " ", "A", "F", "X"]) for _ in range(45))
        print(f"{DARK_GREEN}{linea}{RESET}")
        time.sleep(0.05)
    print(f"{GREEN}[+] Connessione al mainframe stabilita.{RESET}\n")

def banner_ultimate():
    print(f"{MAGENTA}" + "=" * 65 + f"{RESET}")
    print(f"{GREEN}")
    print(r"  __  __   _  _____ _____ ____  __  __ _____ _____ ")
    print(r" |  \/  | / \|_   _|_   _|  _ \|  \/  | ____| ____|")
    print(r" | |\/| |/ _ \ | |   | | | |_) | |\/| |  _| |  _|  ")
    print(r" | |  | / ___ \| |   | | |  _ <| |  | | |___| |___ ")
    print(r" |_|  |/_/   \_\_|   |_| |_| \_\_|  |_|_____|_____|")
    print(f"{RESET}")
    print(f"{MAGENTA}       [ MATRIX NETRUNNER ULTIMATE SUITE v6.0 ]{RESET}")
    print(f"{MAGENTA}" + "=" * 65 + f"{RESET}")
    print(f"{YELLOW}1.{RESET} Scansione Mirata + HTTP Fingerprinting & Metodi HTTP")
    print(f"{YELLOW}2.{RESET} Network Sweep Massivo della Sottorete Locale")
    print(f"{YELLOW}3.{RESET} Disconnessione (Esci dalla Matrix)")
    print(f"{MAGENTA}" + "-" * 65 + f"{RESET}")

def analizza_vulnerabilita_web(target_ip, porta):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.5)
    dettaglio = "Servizio attivo"
    try:
        s.connect((target_ip, porta))
        if porta in [80, 443, 8080, 8443, 5000, 3000]:
            request = f"OPTIONS / HTTP/1.1\r\nHost: {target_ip}\r\nUser-Agent: MatrixUltimate/6.0\r\nConnection: close\r\n\r\n"
            s.sendall(request.encode())
            risposta = s.recv(2048).decode(errors="ignore")
            linee = risposta.split("\r\n")
            header_principale = linee[0] if linee else "HTTP Attivo"
            
            metodi_consentiti = "N/D"
            for linea in linee:
                if linea.lower().startswith("allow:"):
                    metodi_consentiti = linea.split(":")[1].strip()
            
            dettaglio = f"Status: {header_principale} | Metodi Allow: {metodi_consentiti}"
    except Exception:
        pass
    finally:
        s.close()
    return dettaglio

def scansiona_porta(target_ip, porta, risultati_lista):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.4)
    try:
        if s.connect_ex((target_ip, porta)) == 0:
            sfx = random.choice(SFX_LIST)
            info_web = analizza_vulnerabilita_web(target_ip, porta)
            
            msg = f"{GREEN}[{sfx}] {target_ip}:{porta} -> APERTA | {info_web}{RESET}"
            
            item = {
                "ip": target_ip,
                "port": porta,
                "status": "OPEN",
                "details": info_web
            }
            
            with print_lock:
                print(msg)
                risultati_lista.append(item)
    except socket.error:
        pass
    finally:
        s.close()

def ping_host(base_ip, host_num, risultati_lista):
    target_ip = f"{base_ip}.{host_num}"
    common_ports = [21, 22, 80, 443, 3000, 8080]
    for porta in common_ports:
        scansiona_porta(target_ip, porta, risultati_lista)

def main():
    while True:
        banner_ultimate()
        scelta = input(f"{CYAN}Seleziona opzione [1-3]: {RESET}").strip()

        if scelta == "1":
            target_ip = input(f"{YELLOW}Inserisci IP target (es. 127.0.0.1): {RESET}").strip()
            try:
                start_p = int(input(f"{YELLOW}Porta di inizio: {RESET}"))
                end_p = int(input(f"{YELLOW}Porta di fine: {RESET}"))
            except ValueError:
                print(f"{RED}[-] Inserisci coordinate numeriche valide!{RESET}\n")
                continue

            matrix_rain_effect()
            risultati = []
            inizio = time.time()

            with ThreadPoolExecutor(max_workers=100) as executor:
                for porta in range(start_p, end_p + 1):
                    executor.submit(scansiona_porta, target_ip, porta, risultati)

            fine = time.time()
            
            json_file = f"matrix_report_{target_ip.replace('.', '_')}.json"
            with open(json_file, "w") as jf:
                json.dump(risultati, jf, indent=4)

            print(f"\n{GREEN}[✔] Operazione completata in {fine - inizio:.2f} secondi!{RESET}")
            print(f"{MAGENTA}[i] Report salvato in: {json_file}{RESET}\n")
            input("Premi [Invio] per tornare al menu...")

        elif scelta == "2":
            prefisso = input(f"{YELLOW}Inserisci i primi 3 numeri della rete (es. 192.168.1): {RESET}").strip()
            matrix_rain_effect()
            risultati = []
            inizio = time.time()

            with ThreadPoolExecutor(max_workers=50) as executor:
                for host in range(1, 255):
                    executor.submit(ping_host, prefisso, host, risultati)

            fine = time.time()
            json_file = "matrix_network_sweep.json"
            with open(json_file, "w") as jf:
                json.dump(risultati, jf, indent=4)

            print(f"\n{GREEN}[✔] Sweep di rete completato in {fine - inizio:.2f} secondi!{RESET}")
            print(f"{MAGENTA}[i] Report JSON salvato in: {json_file}{RESET}\n")
            input("Premi [Invio] per tornare al menu...")

        elif scelta == "3":
            print(f"\n{MAGENTA}Disconnessione dalla Matrix in corso... Segui il bianconiglio.{RESET}\n")
            sys.exit(0)
        else:
            print(f"\n{RED}[-] Comando non riconosciuto nella griglia.{RESET}\n")

if __name__ == "__main__":
    main()
