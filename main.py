import requests
import time
import random
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# --- ДАНІ ДЛЯ ВХОДУ ---
USER_LOGIN = "Dark Tornado"
USER_PASS = "12334455"

# --- МІНІ-СЕРВЕР ДЛЯ RENDER ---
class SimpleServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_server():
    server = HTTPServer(('0.0.0.0', 10000), SimpleServer)
    server.serve_forever()

# --- ЛОГІКА БОТА ---
class TiwarBot:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36'
        })
        self.base_url = "https://tiwar.ru"

    def login(self):
        print(f"Login attempt: {USER_LOGIN}")
        payload = {'login': USER_LOGIN, 'pass': USER_PASS, 'ok': 'Вход'}
        try:
            res = self.session.post(f"{self.base_url}/login/", data=payload)
            if "Выход" in res.text or "cabinet" in res.text:
                print("SUCCESS: Bot is in game!")
                return True
            print("FAILED: Wrong password or nickname.")
            return False
        except:
            print("FAILED: Server offline.")
            return False

    def play(self):
        print("Fighting in Coliseum...")
        self.session.get(f"{self.base_url}/coliseum/")
        for i in range(3):
            self.session.get(f"{self.base_url}/coliseum/attack/")
            time.sleep(4)
        print("Battle finished.")

    def start(self):
        if not self.login(): return
        while True:
            try:
                self.play()
                self.session.get(f"{self.base_url}/daily_rewards/")
                wait = random.randint(600, 900)
                print(f"Next battle in {wait // 60} minutes.")
                time.sleep(wait)
                if "login" in self.session.get(self.base_url).url:
                    self.login()
            except:
                time.sleep(60)

if __name__ == "__main__":
    # Запускаємо "сайт", щоб Render не лаявся
    threading.Thread(target=run_server, daemon=True).start()
    # Запускаємо бота
    TiwarBot().start()
    
