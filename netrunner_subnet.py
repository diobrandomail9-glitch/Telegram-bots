import socket
import sys
import time
import threading
import random
from concurrent.futures import ThreadPoolExecutor

# Colori ANSI Neon
CYAN = "\033[96m"
GREEN = "\033[92m"
MAGENTA = "\033[95m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

SFX_LIST = ["ZOT!", "DON!", "BZZT!", "KABOOM!", "CRASH!"]
print_lock = threading.Lock()

def banner_matrix():
    print(f"{MAGENTA}" + "=" * 55 + f"{RESET}")
    print(f"{CYAN}")
    print(r"  _   _ _____ _____ ____  _   _ _   _ _   _ _____ ____  ")
    print(r" | \ | | ____|_   _|  _ \| | | | \ | | \ | | ____|  _ \ ")
    print(r" |  \| |  _|   | | | |_) | | | |  \| |  \| |  _| | |_) |")
    print(r" | |\  | |___  | | |  _ <| |_| | |\  | |\  | |___|  _ < ")
    print(r" |_| \_|_____| |_| |_| \_\\___/|_| \_|_| \_|_____|_| \_\ ")
    print(f"{RESET}")
    print(f"{MAGENTA}       [ NETRUNNER SUBNET & MATRIX EDITION v4.0 ]{RESET}")
    print(f"{MAGENTA}" + "=" * 55 + f"{RESET}")
    print(f"{YELLOW}1.{RESET} Scansione Singolo IP (Avanzata + Banner)")
    print(f"{YELLOW}2.{RESET} Scansione Intera Sottorete (Network Sweep)")
    print(f"{YELLOW}3.{RESET} Esci dalla Matrix")
    print(f"{MAGENTA}" + "-" * 55 + f"{RESET}")

def scansiona_porta(target_ip, porta, report_file):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.4)
    try:
        if s.connect_ex((target_ip, porta)) == 0:
            sfx = random.choice(SFX_LIST)
            try:
                s.settimeout(0.8)
                banner = s.recv(512).decode(errors="ignore").strip()
                banner_info = f" | Servizio: {banner}" if banner else " | Servizio attivo"
            except:
                banner_info = " | Servizio attivo (No Banner)"

            msg = f"{GREEN}[{sfx}] {target_ip}:{porta} -> APERTA{banner_info}{RESET}"
            clean_msg = f"[{sfx}] {target_ip}:{porta} -> APERTA{banner_info}"
            
            with print_lock:
                print(msg)
                if report_file:
                    with open(report_file, "a") as f:
                        f.write(clean_msg + "\n")
    except socket.error:
        pass
    finally:
        s.close()

def ping_host(base_ip, host_num, report_file):
    target_ip = f"{base_ip}.{host_num}"
    # Porte chiave da testare velocemente sulla sottorete (es. Web, SSH, Proxy)
    common_ports = [21, 22, 80, 443, 4444, 8080, 8443]
    
    for porta in common_ports:
        scansiona_porta(target_ip, porta, report_file)

def main():
    while True:
        banner_matrix()
        scelta = input(f"{CYAN}Seleziona protocollo [1-3]: {RESET}").strip()

        if scelta == "1":
            target_ip = input(f"{YELLOW}Inserisci IP target (es. 127.0.0.1): {RESET}").strip()
            try:
                start_p = int(input(f"{YELLOW}Porta inizio: {RESET}"))
                end_p = int(input(f"{YELLOW}Porta fine: {RESET}"))
            except ValueError:
                print(f"{RED}[-] Errore di digitazione!{RESET}\n")
                continue

            report_file = "report_subnet_single.txt"
            print(f"\n{CYAN}[!] Avvio attacco mirato su {target_ip} ({start_p}-{end_p})...{RESET}")
            inizio = time.time()

            with open(report_file, "w") as f:
                f.write(f"=== TARGET: {target_ip} ({start_p}-{end_p}) ===\n")

            with ThreadPoolExecutor(max_workers=100) as executor:
                for porta in range(start_p, end_p + 1):
                    executor.submit(scansiona_porta, target_ip, porta, report_file)

            fine = time.time()
            print(f"\n{GREEN}[✔] Operazione chiusa in {fine - inizio:.2f} secondi!{RESET}\n")
            input("Premi [Invio] per continuare...")

        elif scelta == "2":
            prefisso = input(f"{YELLOW}Inserisci i primi 3 numeri della rete (es. 192.168.1): {RESET}").strip()
            report_file = "report_network_sweep.txt"
            
            print(f"\n{CYAN}[!] Scansione massiva della sottorete {prefisso}.1-254 in corso...{RESET}")
            inizio = time.time()

            with open(report_file, "w") as f:
                f.write(f"=== NETWORK SWEEP REPORT: {prefisso}.0/24 ===\n")

            # Scansioniamo gli host da 1 a 254 in parallelo usando i thread
            with ThreadPoolExecutor(max_workers=50) as executor:
                for host in range(1, 255):
                    executor.submit(ping_host, prefisso, host, report_file)

            fine = time.time()
            print(f"\n{GREEN}[✔] Sweep di rete completato in {fine - inizio:.2f} secondi!{RESET}")
            print(f"{MAGENTA}[i] Report globale salvato in: {report_file}{RESET}\n")
            input("Premi [Invio] per continuare...")

        elif scelta == "3":
            print(f"\n{MAGENTA}Uscita dalla simulazione. Stay safe, Netrunner.{RESET}\n")
            sys.exit(0)
        else:
            print(f"\n{RED}[-] Comando errato nella griglia.{RESET}\n")

if __name__ == "__main__":
    main()
