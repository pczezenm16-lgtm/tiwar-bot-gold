import requests
import time
import random

# --- ДАНІ ДЛЯ ВХОДУ ---
USER_LOGIN = "Dark Tornado"
USER_PASS = "12334455"

class TiwarBot:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = "https://tiwar.ru"
        self.is_logged_in = False

    def login(self):
        print(f"[Вхід]: Спроба зайти під ніком {USER_LOGIN}...")
        payload = {
            'login': USER_LOGIN,
            'pass': USER_PASS,
            'ok': 'Вхід'
        }
        try:
            res = self.session.post(f"{self.base_url}/login/", data=payload)
            if "Вихід" in res.text or "Мій кабінет" in res.text:
                print("[Успіх]: Ви зайшли в гру!")
                self.is_logged_in = True
                return True
            else:
                print("[Помилка]: Невірний нік або пароль.")
                return False
        except:
            print("[Помилка]: Сервер гри недоступний.")
            return False

    def play_coliseum(self):
        print("[Колізей]: Починаю бій...")
        self.session.get(f"{self.base_url}/coliseum/")
        for i in range(3):
            self.session.get(f"{self.base_url}/coliseum/attack/")
            print(f"  Удар {i+1} нанесено")
            time.sleep(3)
        print("[Колізей]: Битву завершено.")

    def collect_resources(self):
        print("[Ресурси]: Перевіряю щоденні нагороди...")
        self.session.get(f"{self.base_url}/daily_rewards/") 

    def main_loop(self):
        if not self.login(): return

        while True:
            try:
                self.play_coliseum()
                self.collect_resources()

                wait_time = random.randint(600, 900) # Чекаємо 10-15 хвилин
                print(f"[Сон]: Зайду через {wait_time // 60} хвилин...")
                time.sleep(wait_time) 
                
                # Перевірка сесії
                res = self.session.get(self.base_url)
                if "Вхід" in res.text:
                    self.login()

            except Exception as e:
                print(f"[Помилка]: {e}")
                time.sleep(60)

if __name__ == "__main__":
    bot = TiwarBot()
    bot.main_loop()
  
