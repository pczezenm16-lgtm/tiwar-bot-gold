import requests
import time
import random

# ДАНІ ДЛЯ ВХОДУ (Перевір їх ще раз!)
USER_LOGIN = "Dark Tornado"
USER_PASS = "12334455"

class TiwarBot:
    def __init__(self):
        self.session = requests.Session()
        # Маскуємо бота під звичайний браузер Chrome на Android
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-A505F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36'
        })
        self.base_url = "https://tiwar.ru"

    def login(self):
        print(f"Спроба входу: {USER_LOGIN}")
        payload = {'login': USER_LOGIN, 'pass': USER_PASS, 'ok': 'Вход'}
        try:
            res = self.session.post(f"{self.base_url}/login/", data=payload)
            # Перевіряємо, чи з'явилася кнопка Вихід (це значить ми всередині)
            if "Выход" in res.text or "cabinet" in res.text:
                print("УСПІХ: Бот у грі!")
                return True
            else:
                print("ПОМИЛКА: Гра не прийняла пароль.")
                return False
        except:
            print("ПОМИЛКА: Немає зв'язку з сервером.")
            return False

    def play(self):
        print("Б'юся в Колізеї...")
        self.session.get(f"{self.base_url}/coliseum/")
        for i in range(3):
            self.session.get(f"{self.base_url}/coliseum/attack/")
            print(f"Удар {i+1}")
            time.sleep(random.randint(3, 6))

    def start(self):
        if not self.login(): return
        while True:
            try:
                self.play()
                # Збір нагород
                self.session.get(f"{self.base_url}/daily_rewards/")
                
                wait = random.randint(600, 900) # 10-15 хвилин
                print(f"Відпочинок {wait // 60} хв...")
                time.sleep(wait)
                
                # Якщо вилетіли — заходимо знову
                if "login" in self.session.get(self.base_url).url:
                    self.login()
            except Exception as e:
                print(f"Помилка циклу: {e}")
                time.sleep(60)

if __name__ == "__main__":
    TiwarBot().start()
    
