import speech_recognition as sr
import webbrowser
import re
import requests
import bs4
from selenium import webdriver

# -------------------------------Googler---------------------------------------
def googler(to_search_for):  # opens a google page in a new window
    search = to_search_for

    try:
        print("Searching on Google...")

        # How many tabs should be open? Code
        how_many_tabs = 1
        list = []
        if not re.findall(r'\+\+(\w+)', search):
            print("Finding top result for " + "'" + search + "'" + " ...")
        if re.findall(r'\+\+(\w+)', search):
            list = re.findall(r'\+\+(\w+)', search)
            if int(list[0]):
                how_many_tabs = int(list[0])
                search, separator, old_string = search.partition(
                    '++' + list[0])
                print("Finding top " + str(how_many_tabs) +
                      " results for " + "'" + search + "'" + " ...")

        # Opening the tabs
        res = requests.get('https://google.com/search?q=' + search)
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        links = soup.select('.r a')
        num_tabs = min(how_many_tabs, len(links))

        for i in range(num_tabs):
            webbrowser.open('https://google.com' + links[i].get('href'))

    except Exception as e:
        print(e)
