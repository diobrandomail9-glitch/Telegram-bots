import socket
import sys
import time
import threading
import random
from concurrent.futures import ThreadPoolExecutor

# Colori ANSI Neon per lo stile Cyberpunk/Manga
CYAN = "\033[96m"
GREEN = "\033[92m"
MAGENTA = "\033[95m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"

# Onomatopee in stile manga per le porte trovate
SFX_LIST = ["ZOT!", "DON!", "BZZT!", "KABOOM!", "SPARK!", "WHAM!"]

print_lock = threading.Lock()

def banner_manga():
    print(f"{MAGENTA}" + "=" * 50 + f"{RESET}")
    print(f"{CYAN}")
    print(r"  _   _ _____ _____ ____  _   _ _   _ _   _ _____ ____  ")
    print(r" | \ | | ____|_   _|  _ \| | | | \ | | \ | | ____|  _ \ ")
    print(r" |  \| |  _|   | | | |_) | | | |  \| |  \| |  _| | |_) |")
    print(r" | |\  | |___  | | |  _ <| |_| | |\  | |\  | |___|  _ < ")
    print(r" |_| \_|_____| |_| |_| \_\\___/|_| \_|_| \_|_____|_| \_\ ")
    print(f"{RESET}")
    print(f"{MAGENTA}       [ NETRUNNER TERMUX EDITION v3.5 ]{RESET}")
    print(f"{MAGENTA}" + "=" * 50 + f"{RESET}")
    print(f"{YELLOW}1.{RESET} Scansione Rapida (Porte 1-1024)")
    print(f"{YELLOW}2.{RESET} Scansione Avanzata + Banner Grabbing (Custom)")
    print(f"{YELLOW}3.{RESET} Esci dalla Matrix")
    print(f"{MAGENTA}" + "-" * 50 + f"{RESET}")

def scansiona_porta(target_ip, porta, usa_banner, report_file):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        if s.connect_ex((target_ip, porta)) == 0:
            info_banner = ""
            if usa_banner:
                try:
                    s.settimeout(1.0)
                    banner = s.recv(1024).decode(errors="ignore").strip()
                    if banner:
                        info_banner = f" | Banner: {banner}"
                    else:
                        info_banner = " | Banner: Nessun banner esplicito"
                except:
                    info_banner = " | Banner: Timeout"

            sfx = random.choice(SFX_LIST)
            msg = f"{GREEN}[{sfx}] Porta {porta} APERTA!{info_banner}{RESET}"
            clean_msg = f"[{sfx}] Porta {porta} APERTA!{info_banner}"
            
            with print_lock:
                print(msg)
                if report_file:
                    with open(report_file, "a") as f:
                        f.write(clean_msg + "\n")
    except socket.error:
        pass
    finally:
        s.close()

def main():
    while True:
        banner_manga()
        scelta = input(f"{CYAN}Seleziona comando [1-3]: {RESET}").strip()

        if scelta == "1":
            target_ip = input(f"{YELLOW}Inserisci IP target (es. 127.0.0.1): {RESET}").strip()
            report_file = "report_manga_standard.txt"
            
            print(f"\n{CYAN}[!] Infiltrazione in corso su {target_ip} (1-1024)...{RESET}")
            inizio = time.time()

            with open(report_file, "w") as f:
                f.write(f"=== MANGA SCAN REPORT (STANDARD) ===\nTarget: {target_ip}\n-----------------------------------\n")

            with ThreadPoolExecutor(max_workers=100) as executor:
                for porta in range(1, 1025):
                    executor.submit(scansiona_porta, target_ip, porta, False, report_file)

            fine = time.time()
            print(f"\n{GREEN}[✔] Operazione completata in {fine - inizio:.2f} secondi!{RESET}")
            print(f"{MAGENTA}[i] Log salvato in: {report_file}{RESET}\n")
            input("Premi [Invio] per tornare al menu principale...")

        elif scelta == "2":
            target_ip = input(f"{YELLOW}Inserisci IP target (es. 127.0.0.1): {RESET}").strip()
            try:
                start_port = int(input(f"{YELLOW}Porta di inizio (es. 1): {RESET}"))
                end_port = int(input(f"{YELLOW}Porta di fine (es. 9000): {RESET}"))
            except ValueError:
                print(f"{RED}[-] Errore critico: Inserisci coordinate numeriche valide!{RESET}\n")
                continue

            report_file = "report_manga_custom.txt"
            print(f"\n{CYAN}[!] Scansione profonda + Interrogazione dati su {target_ip} ({start_port}-{end_port})...{RESET}")
            inizio = time.time()

            with open(report_file, "w") as f:
                f.write(f"=== MANGA SCAN REPORT (ADVANCED) ===\nTarget: {target_ip} | Range: {start_port}-{end_port}\n-----------------------------------\n")

            with ThreadPoolExecutor(max_workers=100) as executor:
                for porta in range(start_port, end_port + 1):
                    executor.submit(scansiona_porta, target_ip, porta, True, report_file)

            fine = time.time()
            print(f"\n{GREEN}[✔] Operazione completata in {fine - inizio:.2f} secondi!{RESET}")
            print(f"{MAGENTA}[i] Log salvato in: {report_file}{RESET}\n")
            input("Premi [Invio] per tornare al menu principale...")

        elif scelta == "3":
            print(f"\n{MAGENTA}Disconnessione dalla rete in corso... Sayonara!{RESET}\n")
            sys.exit(0)
        else:
            print(f"\n{RED}[-] Comando non riconosciuto nella Matrix. Riprova.{RESET}\n")

if __name__ == "__main__":
    main()
