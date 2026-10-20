import socket
import sys
import time

target_ip = input("Inserisci l'IP da scansionare (es. 127.0.0.1): ")
start_port = int(input("Inserisci la porta di inizio (es. 1): "))
end_port = int(input("Inserisci la porta di fine (es. 9000): "))

print(f"\nSto avviando la scansione su {target_ip} (dalla porta {start_port} alla {end_port})...")

# Registriamo il tempo di inizio
inizio = time.time()

for target_port in range(start_port, end_port + 1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.3)
    
    try:
        result = s.connect_ex((target_ip, target_port))
        if result == 0:
            print(f"[+] Trovata! La porta {target_port} è APERTA")
    except socket.error:
        pass
    finally:
        s.close()

# Calcoliamo il tempo totale impiegato
fine = time.time()
tempo_totale = fine - inizio

print(f"\nScansione completata in {tempo_totale:.2f} secondi!")
