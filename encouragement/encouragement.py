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


def analyze(user, sources):
    # 1st priority: word count for content, 2nd priority: emotion detection
    userInput = user.split(" ")

    userDict = {}
    sourceDict = {}
    for word in userInput:
        if(len(word) > 2 and word != "the" and word != "and" and word != ""):
            if word not in userDict.keys():
                userDict[word] = 1
            else:
                userDict[word] = userDict[word]+1

    # analyze by relevant words count
    count = 0
    score = 0
    for source in sources:
        words_in_source = source.split(" ")
        for word in userDict.keys():
            if(word in words_in_source):
                score = score + 1
        sourceDict[count] = score
        count = count + 1
        score = 0

    max = 0
    i = 0
    # Get the index with the highest score
    for index in sourceDict.keys():
        if sourceDict[index] > max:
            max = sourceDict[index]
            i = index

    # Refer back to the index in sourceDict
    response = sources[i]

    return response


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

    # testCase
    userInput = "I feel completely empty today. Things just didn't work out. Work didn't go well. My head wasn't working right. My parents got mad at me for something I didn't do.."
    print(analyze(userInput, all))

    print(analyze(userInput, bible_verses))
    print(analyze(userInput, motiv_quotes))

    # csv_file = open('verses.csv', 'w')
    # csv_writer = csv.writer(csv_file)

    # for verse in bible_verses:
    #     csv_writer.writerow(verse)

    # csv_file.close()


main()
