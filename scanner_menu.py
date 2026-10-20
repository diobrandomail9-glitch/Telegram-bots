import socket
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor

print_lock = threading.Lock()

def banner_principale():
    print("=" * 45)
    print("      PYTHON CYBER SECURITY SCANNER v3.0")
    print("=" * 45)
    print("1. Scansione rapida standard (Porte 1-1024)")
    print("2. Scansione personalizzata (Intervallo + Banner Grabbing)")
    print("3. Esci")
    print("-" * 45)

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

            msg = f"[+] Porta {porta} APERTA{info_banner}"
            with print_lock:
                print(msg)
                if report_file:
                    with open(report_file, "a") as f:
                        f.write(msg + "\n")
    except socket.error:
        pass
    finally:
        s.close()

def main():
    while True:
        banner_principale()
        scelta = input("Seleziona un'opzione (1-3): ").strip()

        if scelta == "1":
            target_ip = input("Inserisci l'IP da scansionare (es. 127.0.0.1): ").strip()
            report_file = "report_standard.txt"
            
            print(f"\n[i] Avvio scansione standard su {target_ip} (1-1024)...")
            inizio = time.time()

            with open(report_file, "w") as f:
                f.write(f"=== REPORT STANDARD ===\nTarget: {target_ip}\n-----------------------------------\n")

            with ThreadPoolExecutor(max_workers=100) as executor:
                for porta in range(1, 1025):
                    executor.submit(scansiona_porta, target_ip, porta, False, report_file)

            fine = time.time()
            print(f"\n[✔] Scansione completata in {fine - inizio:.2f} secondi.")
            print(f"[i] Report salvato in: {report_file}\n")
            input("Premi Invio per tornare al menu...")

        elif scelta == "2":
            target_ip = input("Inserisci l'IP da scansionare (es. 127.0.0.1): ").strip()
            try:
                start_port = int(input("Porta iniziale (es. 1): "))
                end_port = int(input("Porta finale (es. 9000): "))
            except ValueError:
                print("[-] Errore: Inserisci numeri validi per le porte!\n")
                continue

            report_file = "report_custom.txt"
            print(f"\n[i] Avvio scansione avanzata con Banner Grabbing su {target_ip} ({start_port}-{end_port})...")
            inizio = time.time()

            with open(report_file, "w") as f:
                f.write(f"=== REPORT CUSTOM + BANNER ===\nTarget: {target_ip} | Range: {start_port}-{end_port}\n-----------------------------------\n")

            with ThreadPoolExecutor(max_workers=100) as executor:
                for porta in range(start_port, end_port + 1):
                    executor.submit(scansiona_porta, target_ip, porta, True, report_file)

            fine = time.time()
            print(f"\n[✔] Scansione completata in {fine - inizio:.2f} secondi.")
            print(f"[i] Report salvato in: {report_file}\n")
            input("Premi Invio per tornare al menu...")

        elif scelta == "3":
            print("\nChiusura del programma. A presto!")
            sys.exit(0)
        else:
            print("\n[-] Scelta non valida. Riprova.\n")

if __name__ == "__main__":
    main()
