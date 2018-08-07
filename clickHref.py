import speech_recognition as sr
import webbrowser
import re
import requests
import bs4
import os
from selenium import webdriver

# Setting up the Chrome Selenium Webdriver and getting PATHs setup for easy access later with "global"
currentDirectory = os.path.dirname(__file__)

soundDirectory = currentDirectory + r"/sounds//"
chromedriverPath = currentDirectory + "/setup/chromedriver.exe"
setupPath = currentDirectory + "\setup\\"  # USE AS GLOBAL VARIABLE

input("1")
options = webdriver.ChromeOptions()
options.add_argument(r"user-data-dir=C:\Users\Minjea\AppData\Local\Google\Chrome\User Data") #Path to your chrome profile
input("2")

driver = webdriver.Chrome(chromedriverPath, chrome_options=options)

input("Start")

driver.get("youtube.com")
def clickHref(search_for):
    global driver
    input("Trying1")
    try:
        input("Trying2")
        driver.get("https://www.youtube.com/watch?v=YQHsXMglC9A")
        print(driver.current_url)
        # Opening the tabs
        # input("1")
        res = requests.get(driver.current_url)
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        # input("2")
        links = str(soup.find_all('a')).split(",")
        search_term = search_for
        click_link = ""

        print(links)
        for i in links:
            # print(i)
            if search_term.lower() in i.lower():
                i = i.split()
                print(i)
                for link in i:
                    if "href" in link:
                        click_link = link[6:len(link) - 1]
        print("THIS IS CLICK_LINK: ", click_link)

        if ".com" not in click_link and ".org" not in click_link:
            driverURL = driver.current_url.split(".com")
            print(driverURL)
            goToLink = driverURL[0] + ".com" + click_link
        print(goToLink)

        input("Go to link")
        driver.get(goToLink)


    except Exception as e:
        print(e)

clickHref("someone like you")