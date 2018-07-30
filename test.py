import os
import selenium
from selenium import webdriver
import time
currentDirectory = os.path.dirname(__file__)
soundDirectory = currentDirectory + r"/sounds//"
chromedriverPath = currentDirectory + "/setup/chromedriver.exe"
driver = webdriver.Chrome(chromedriverPath)

<<<<<<< HEAD
driver.get("https://www.youtube.com/watch?v=OwJPPaEyqhI")

input("enter")
link = driver.find_element_by_id("Ylvis - The Fox (What Does The Fox Say?) [Official music video HD]")

link.click()
=======
driver.get("https://youtube.com")
input("enter")
num = 0
scroll = str(270)
while True:
    input("enter")
    try:
        print("window.scrollTo(0, " + scroll + ");")
        driver.execute_script("window.scrollTo(0, " + scroll + ");")
    except Exception as e:
        print(e)
    num += 270
    scroll = str(num)
>>>>>>> 981cdd378eeebd3294357b41f4428aeded3f2ea9
