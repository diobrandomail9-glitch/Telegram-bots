import time
import requests

TOKEN = "8968190359:AAF60j6nsjIJztTv9ewJgDVzQ141VpLMK9Q"
MIO_CHAT_ID = "7051087231"
offset = 0

print("Avvio monitoraggio iscritti in corso...")

while True:
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset={offset}&timeout=30"
        response = requests.get(url).json()
        
        if "result" in response:
            for update in response["result"]:
                offset = update["update_id"] + 1
                
                # Controlla se c'è un evento di nuovo membro nel canale o gruppo
                chat_member = update.get("chat_member") or update.get("my_chat_member")
                if chat_member:
                    new_status = chat_member.get("new_chat_member", {}).get("status")
                    user = chat_member.get("new_chat_member", {}).get("user", {})
                    
                    if new_status == "member":
                        nome = user.get("first_name", "Utente")
                        username = user.get("username", "Nessuno")
                        
                        # Invia la notifica a te stesso
                        msg = f"🔔 Nuovo iscritto!\nNome: {nome}\nUsername: @{username}"
                        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data={
                            "chat_id": MIO_CHAT_ID,
                            "text": msg
                        })
    except Exception as e:
        print(f"Errore nel polling iscritti: {e}")
        time.sleep(10)
        
    time.sleep(5)
