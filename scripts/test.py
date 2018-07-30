
from selenium import webdriver
import time
import os

currentDirectory = os.path.dirname(__file__).replace("scripts", "")
chromedriverPath = currentDirectory + "\setup\chromedriver.exe"

driver = chromedriverPath


driver = webdriver.Chrome(driver)



# driver.set_window_position(-10000, 0)

driver.get("https://www.youtube.com/")
input("Press enter")
try:
    element = driver.find_element_by_id("search")
    element.send_keys("hello adele")
    element.send_keys(u'\ue007')
except Exception as f0:
    print(f0)

