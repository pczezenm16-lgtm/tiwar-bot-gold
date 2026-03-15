import requests
import time
import random

# Вписуй дані ТІЛЬКИ в лапках нижче:
NICK = "Dark Tornado"
PASS = "12334455"

class TiwarBot:
    def __init__(self):
        self.session = requests.Session()
        self.url = "https://tiwar.ru"

    def login(self):
        print(f"Connecting as: {NICK}")
        # Ці дані не можна перекладати!
        data = {'login': NICK, 'pass': PASS, 'ok': 'Вход'}
        try:
            r = self.session.post(f"{self.url}/login/", data=data)
            if "Выход" in r.text or "кабинет" in r.text:
                print("SUCCESS: Logged in!")
                return True
            print("ERROR: Login failed. Check Nick/Pass.")
            return False
        except:
            print("ERROR: Server unreachable.")
            return False

    def play(self):
        print("Coliseum battle...")
        self.session.get(f"{self.url}/coliseum/")
        for i in range(3):
            self.session.get(f"{self.url}/coliseum/attack/")
            print(f"Hit {i+1}")
            time.sleep(random.randint(3, 5))

    def start(self):
        if not self.login(): return
        while True:
            try:
                self.play()
                # Збір ресурсів
                self.session.get(f"{self.url}/daily_rewards/")
                
                wait = random.randint(600, 900)
                print(f"Sleeping {wait // 60} min...")
                time.sleep(wait)
                
                # Перевірка, чи ми ще в грі
                check = self.session.get(self.url)
                if "Вход" in check.text:
                    self.login()
            except Exception as e:
                print(f"Loop error: {e}")
                time.sleep(60)

if __name__ == "__main__":
    TiwarBot().start()
    
