import socket
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor

# Controllo argomenti: IP obbligatorio, porte di inizio e fine opzionali
if len(sys.argv) < 2:
    print("[-] Uso corretto: python scanner_pro.py <IP> [porta_inizio] [porta_fine]")
    print("[-] Esempio: python scanner_pro.py 127.0.0.1 1 1024")
    sys.exit(1)

target_ip = sys.argv[1]
start_port = int(sys.argv[2]) if len(sys.argv) > 2 else 1
end_port = int(sys.argv[3]) if len(sys.argv) > 3 else 1024

report_file = "report_pro.txt"
print_lock = threading.Lock()

print(f"\n[i] Scansione avanzata avviata su {target_ip} (Porte: {start_port}-{end_port})")
inizio = time.time()

with open(report_file, "w") as f:
    f.write(f"=== REPORT ADVANCED SCAN ===\n")
    f.write(f"Target: {target_ip} | Range: {start_port}-{end_port}\n")
    f.write("-" * 45 + "\n")

def scansiona_porta(porta):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        if s.connect_ex((target_ip, porta)) == 0:
            banner = "N/D"
            # Tentativo di Banner Grabbing (ascoltiamo cosa risponde il servizio)
            try:
                s.settimeout(1.0)
                # Inviamo un piccolo "saluto" o leggiamo direttamente se il servizio parla per primo
                banner = s.recv(1024).decode(errors="ignore").strip()
                if not banner:
                    banner = "Connessione stabilita (Nessun banner esplicito)"
            except:
                banner = "Servizio attivo (Timeout banner)"

            msg = f"[+] Porta {porta} APERTA | Banner: {banner}"
            with print_lock:
                print(msg)
                with open(report_file, "a") as f:
                    f.write(msg + "\n")
    except socket.error:
        pass
    finally:
        s.close()

with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(scansiona_porta, range(start_port, end_port + 1))

fine = time.time()
print(f"\n[✔] Scansione completata in {fine - inizio:.2f} secondi.")
print(f"[i] Report salvato in: {report_file}")
