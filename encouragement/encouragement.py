from bs4 import BeautifulSoup
import requests
import csv
import string
import os
import time
import datetime
from gtts import gTTS
import os

import pygame


def analyze(news):
    ########################
    # Sentimental Analysis #
    ########################
    count = 0
    neg = 0.0
    pos = 0.0
    neutral = 0.0
    second_filter = (list("~!@#$%^&*()_-+=1234567890{}[]\|?/><,.;:'"))
    templist = [""]
    for i in range(1, len(news)):
        temp_neg = 0.0
        temp_pos = 0.0
        temp_neutral = 0.0
        ##############
        # Filtration #
        ##############
        for ch in second_filter:
            if ch in news[i]:
                news[i] = news[i].replace(ch, "")
        if(news[i] != ""):
            info = os.popen("curl -d"+" 'text="+news[i]+"' " +
                            "http://text-processing.com/api/sentiment/").read()
            ###############################
            # Actual Sentimental Analysis #
            ###############################
            if(info.index("neg") != None and info.index("pos") != None and info.index("neutral") != None):
                temp_neg = temp_neg + \
                    float(info[info.index("neg")+6:info.index("neg")+18])
                temp_pos = temp_pos + \
                    float(info[info.index("pos")+6:info.index("pos")+18])
                temp_neutral = temp_neutral + \
                    float(info[info.index("neutral") +
                               10:info.index("neutral")+22])

        templist.append([temp_pos, temp_neg, temp_neutral])
        neg = neg + temp_neg
        pos = pos + temp_pos
        neutral = neutral + temp_neutral
        count = count+1
    all = ["", [neg, pos, neutral]]
    return templist, all


def calcOverall(data):
    if data != "":
        if(data[0] > data[1] and data[0] > data[2]):
            return "Overall Positive ("+str(data)+")"
        elif data[1] > data[0] and data[1] > data[2]:
            return "Overall Negative ("+str(data)+")"
        else:
            if data[1] > data[0]:
                return "Overall Neutral - Slight Negative("+str(data)+")"
            elif data[0] > data[1]:
                return "Overall Neutral - Slight Positive("+str(data)+")"
            else:
                return "Overall Neutral ("+str(data)+")"

    else:
        return ""


def scrape():
    printable = set(string.printable)
    now = datetime.datetime.now()

    # csv_file = open('news'+now.strftime("%Y-%m-%d %H:%M")+'.csv', 'w')
    # csv_writer = csv.writer(csv_file)
    # csv_writer.writerow(['NYTimes', "NY_individual", 'NY_Overall', 'WashingtonPost', 'WP_individual', 'WP_Overall',
    #                      'FoxNews', 'FN_individual', 'FN_Overall', 'WallStreet', 'WS_individual', 'WS_Overall'])
    ny = [""]
    wp = [""]
    fn = [""]
    ws = [""]

    limit = 5
    # New York Times #
    count = 0
    try:
        # source = requests.get(
        #     "https://www.biblestudytools.com/topical-verses/inspirational-bible-verses/").text
        # soup = BeautifulSoup(source, 'lxml')

        # for article in soup.find_all('div', class_='scripture'):
        #     if(count < limit):
        #         tts = gTTS(text=article.text, lang='en')
        #         print(article.text[2:].lstrip())
        #         tts.save("good"+str(count)+".mp3")
        #     count = count + 1
        for i in range(0, count + 1):
            print "hello0"
            pygame.mixer.music.load(os.path.join(
                "/Users/SJP/Documents/personaldev/jarvis/", "good"+str(i)+".mp3"))
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue

            print "hello2"

            continue
    except (requests.ConnectionError):
        print ("ERROR. Invalid URL for NYTimes!")

        # csv_writer.writerow(
        #     [ny_article, ny_article_data, calcOverall(ny_label), wp_article, wp_article_data, calcOverall(wp_label), fn_article, fn_article_data, calcOverall(fn_label), ws_article, ws_article_data, calcOverall(ws_label)])

    # csv_file.close()


start_time = time.time()
pygame.init()
scrape()
print("--- %s seconds ---" % (time.time() - start_time))
