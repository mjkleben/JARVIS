from bs4 import BeautifulSoup
import requests
import csv
import string
import os
import time
import datetime


def getBibleVerses(site):
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


def getMotivQuotes(site):
    printable = set(string.printable)
    array = []
    source = requests.get(
        site).text
    soup = BeautifulSoup(source, 'lxml')

    for verse in soup.find_all('a'):
        if verse.text != "" and len(verse.text.split(" ")) > 4:
            array.append(''.join(filter(lambda x: x in printable, verse.text.encode(
                "utf-8").replace("\r", "").replace("\n", "").replace("  ", ""))))
    return array


def analyze(user, source):
    # 1st priority: word count for content, 2nd priority: emotion detection


def main():
    bible_verses = []
    motiv_quotes = []
    all = []
    bible_sources = [
        "https://www.biblestudytools.com/topical-verses/inspirational-bible-verses/", "https://www.biblestudytools.com/topical-verses/encouraging-bible-verses/", "https://www.biblestudytools.com/topical-verses/peace-bible-verses/", "https://www.biblestudytools.com/topical-verses/faith-bible-verses/", "https://www.biblestudytools.com/topical-verses/worry-and-anxiety-bible-verses/", "https://www.biblestudytools.com/topical-verses/bible-verses-about-blessings/", "https://www.biblestudytools.com/topical-verses/bible-verses-to-comfort-you/", "https://www.biblestudytools.com/topical-verses/bible-verses-about-protection/", "https://www.biblestudytools.com/topical-verses/forgiveness-bible-verses/", "https://www.biblestudytools.com/topical-verses/strength-bible-verses/"]
    motiv_sources = ["https://www.brainyquote.com/topics/motivational",
                     "https://www.brainyquote.com/topics/success", "https://www.brainyquote.com/topics/strength", "https://www.brainyquote.com/topics/anger", "https://www.brainyquote.com/topics/alone", "https://www.brainyquote.com/topics/failure"]

    for source in bible_sources:
        bible_verses.extend(getBibleVerses(source))
    for source in motiv_sources:
        motiv_quotes.extend(getMotivQuotes(source))

    all = bible_verses
    all.extend(motiv_quotes)
    print all
    # csv_file = open('verses.csv', 'w')
    # csv_writer = csv.writer(csv_file)

    # for verse in bible_verses:
    #     csv_writer.writerow(verse)

    # csv_file.close()


main()
