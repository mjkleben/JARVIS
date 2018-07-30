import os
import selenium
from selenium import webdriver
import time
currentDirectory = os.path.dirname(__file__)
soundDirectory = currentDirectory + r"/sounds//"
chromedriverPath = currentDirectory + "/setup/chromedriver.exe"
driver = webdriver.Chrome(chromedriverPath)

driver.get("https://www.youtube.com/watch?v=OwJPPaEyqhI")

input("enter")
link = driver.find_element_by_id("Ylvis - The Fox (What Does The Fox Say?) [Official music video HD]")

link.click()
