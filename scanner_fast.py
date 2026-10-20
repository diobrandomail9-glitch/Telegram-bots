import socket
import sys
import time
import threading
from concurrent.futures import ThreadPoolExecutor

if len(sys.argv) < 2:
    print("[-] Uso corretto: python scanner_fast.py <INDIRIZZO_IP>")
    sys.exit(1)

target_ip = sys.argv[1]
report_file = "report.txt"
print_lock = threading.Lock()

print(f"\n[i] Scansione ultra-veloce avviata su: {target_ip}")
inizio = time.time()

# Inizializziamo il file di report pulendo la vecchia versione
with open(report_file, "w") as f:
    f.write(f"=== REPORT SCANSIONE DIRETTA ===\n")
    f.write(f"Target: {target_ip}\n")
    f.write("-" * 35 + "\n")

def scansiona_porta(porta):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.3)
    try:
        if s.connect_ex((target_ip, porta)) == 0:
            msg = f"[+] Porta {porta} APERTA"
            # Usiamo un Lock per evitare che i thread sovrappongano la scrittura su file e schermo
            with print_lock:
                print(msg)
                with open(report_file, "a") as f:
                    f.write(msg + "\n")
    except socket.error:
        pass
    finally:
        s.close()

# Esecuzione parallela con ThreadPoolExecutor
with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(scansiona_porta, range(1, 1025))

fine = time.time()
print(f"\n[✔] Fatto! Completato in {fine - inizio:.2f} secondi.")
print(f"[i] I risultati sono stati salvati nel file: {report_file}")
