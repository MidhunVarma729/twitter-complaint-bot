from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import os

load_dotenv()

MY_MAIL = os.getenv('MY_MAIL')
MY_PASSWORD = os.getenv('MY_PASSWORD')
PROMISED_DOWN = 100
PROMISED_UP = 20
CHROME_DRIVER_PATH = r"C:\Users\midhu\Downloads\chromedriver_win32\chromedriver.exe"

class InternetSpeedTwitterBot:
    def __init__(self) -> None:
        self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_PATH)
        self.down = 0
        self.up = 0

    def get_internet_speed(self):
        self.driver.maximize_window()
        self.driver.get(r'https://www.speedtest.net/')
        sleep(5)
        start_button = self.driver.find_element(By.CSS_SELECTOR,
            '.start-button .test-mode-multi')
        start_button.click()

        result_displayed = False

        while result_displayed == False:
            try:
                self.driver.find_element(By.CSS_SELECTOR,
                    '.result-container-speed-active .download-speed').text
            except NoSuchElementException:
                sleep(5)
            else:
                self.down = float(
                    self.driver.find_element(By.CSS_SELECTOR,'.result-container-speed-active .download-speed').text)
                self.up = float(
                    self.driver.find_element(By.CSS_SELECTOR, '.result-container-speed-active .upload-speed').text)
                result_displayed = True

    def tweet_at_provider(self):
        self.driver.maximize_window()
        self.driver.get(r'https://twitter.com/i/flow/login')
        sleep(3)
        box = self.driver.find_element(By.XPATH,
            '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
        box.send_keys(MY_MAIL)
        box.send_keys(Keys.ENTER)
        sleep(5)
        box = self.driver.find_element(By.XPATH,
            '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
        box.send_keys(MY_PASSWORD)
        box.send_keys(Keys.ENTER)
        sleep(5)
        tweet = self.driver.find_element(By.CSS_SELECTOR,
            'a[href="/compose/tweet"]')
        tweet.click()
        tweet_box = self.driver.find_element(By.CSS_SELECTOR,
            'div[role="textbox"]')
        tweet_box.send_keys(
            f'Hey Internet provider, why is my internet speed {self.down}down/{self.up}up when I pay for {PROMISED_DOWN}down/{PROMISED_UP}up?')
        tweet = self.driver.find_element(By.CSS_SELECTOR,
            'div[data-testid="tweetButton"]')
        tweet.click()
        self.driver.close()
