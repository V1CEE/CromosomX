import time
from selenium import webdriver as wd
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from System import InsidePath as ip


class SeleniumUtils:
    driver = None
    websiteUrl = None

    def __init__(self, websiteUrl: str):
        options = wd.ChromeOptions()
        options.binary_location ="C:\Program Files\Google\Chrome\Application\chrome.exe"
        chrome_driver_binary = r"C:\Users\shake\PycharmProjects\pythonProject\SeleniumDriver\chromedriver_win32\chromedriver.exe"
        self.driver = wd.Chrome(chrome_driver_binary, chrome_options=options)
        self.websiteUrl = websiteUrl

    def OpenWebsite(self):
        self.driver.get(self.websiteUrl)

    def OpenPage(self):
        self.driver.get(self.PageUrl)

    def WaitElement(self, xpath: str):
        waitSecond = 0.5
        WebDriverWait(self.driver, waitSecond) \
            .until(EC.presence_of_element_located((By.XPATH, xpath)))

    def FindElementByXPATH(self, xpath: str):
        return self.driver.find_element(By.XPATH,xpath)

    def __del__(self):
        pass