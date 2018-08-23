from bs4 import BeautifulSoup
import requests
import csv
import string
import os
import time
import datetime


def getVerses(site):
    printable = set(string.printable)
    array = []
    source = requests.get(
        site).text
    soup = BeautifulSoup(source, 'lxml')

    for verse in soup.find_all('span'):
        if verse.text != "" and len(verse.text.split(" ")) > 7:
            array.append(''.join(filter(lambda x: x in printable, verse.text.encode(
                "utf-8").replace("\r", "").replace("\n", "").replace("  ", "")[2:])))
    return array


def main():
    all_verses = []
    sources = [
        "https://www.biblestudytools.com/topical-verses/inspirational-bible-verses/", "https://www.biblestudytools.com/topical-verses/encouraging-bible-verses/", "https://www.biblestudytools.com/topical-verses/peace-bible-verses/", "https://www.biblestudytools.com/topical-verses/faith-bible-verses/", "https://www.biblestudytools.com/topical-verses/worry-and-anxiety-bible-verses/", "https://www.biblestudytools.com/topical-verses/bible-verses-about-blessings/", "https://www.biblestudytools.com/topical-verses/bible-verses-to-comfort-you/", "https://www.biblestudytools.com/topical-verses/bible-verses-about-protection/", "https://www.biblestudytools.com/topical-verses/forgiveness-bible-verses/", "https://www.biblestudytools.com/topical-verses/strength-bible-verses/"]
    for source in sources:
        all_verses.extend(getVerses(source))

    print all_verses
    # csv_file = open('verses.csv', 'w')
    # csv_writer = csv.writer(csv_file)

    # for verse in array:
    #     print verse
    #     csv_writer.writerow(verse)

    # csv_file.close()
main()
