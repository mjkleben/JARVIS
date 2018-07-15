from bs4 import BeautifulSoup
import requests
import csv
import string
from sa import main
import os
import time


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
        for word in news[i].split(" "):
            for ch in second_filter:
                if ch in word:
                    word = word.replace(ch, "")
            if(word != ""):
                print(word)
                print(len(word))
                print news[i]
                print type(news[i].encode("utf-8"))

                info = os.popen("curl -d"+" text={} ".format(word) +
                                "http://text-processing.com/api/sentiment/").read()
                print info
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
    all = [neg, pos, neutral]
    return templist, all


def scrape():
    printable = set(string.printable)

    csv_file = open('news.csv', 'w')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['NYTimes', "NY_individual", 'WashingtonPost', 'WP_individual'
                         'FoxNews', 'FN_individual', 'WallStreet', 'WS_individual'])
    ny = [""]
    wp = [""]
    fn = [""]
    ws = [""]

    limit = 10
    # New York Times #
    count = 0
    try:
        source = requests.get("https://www.nytimes.com/").text
        soup = BeautifulSoup(source, 'lxml')

        for article in soup.find_all('article'):
            if(count < limit):
                for header in article.find_all('a'):
                    if(header.text and 'Comments' not in header.text and '\n' not in header.text and len(header.text.split(" ")) > 4):
                        ny.append(
                            ''.join(filter(lambda x: x in printable, header.text)))
                count = count + 1

    except (requests.ConnectionError):
        print ("ERROR. Invalid URL for NYTimes!")

    # Washington Post #
    count = 0
    try:
        source = requests.get(
            "https://www.washingtonpost.com/?noredirect=on").text
        soup = BeautifulSoup(source, 'lxml').find(
            'section', id='main-content')
        headlines = soup.find_all('div', class_='headline')
        for headline in headlines:
            if(count < limit):
                if('\n' not in headline.a.text):
                    wp.append(
                        ''.join(filter(lambda x: x in printable, headline.a.text)))
                count = count + 1
    except (requests.ConnectionError):
        print ("ERROR. Invalid URL for WashingtonPost!")

    # Fox News #
    count = 0
    try:
        source = requests.get(
            "https://www.foxnews.com/").text
        soup = BeautifulSoup(source, 'lxml').find(
            'div', class_='main main-primary js-river')
        articles = soup.find_all('a')
        for a in articles:
            if(count < limit):
                if a.text and len(a.text.split(" ")) > 3 and '\n' not in a.text:
                    fn.append(''.join(filter(lambda x: x in printable, a.text)))
            count = count + 1

    except (requests.ConnectionError):
        print ("ERROR. Invalid URL for WashingtonPost!")

    # Wall Street #
    count = 0
    try:
        source = requests.get(
            "https://www.wsj.com/").text
        soup = BeautifulSoup(source, 'lxml').find(
            'div', class_='cb-row')
        articles = soup.find_all('a')
        for a in articles:
            if(count < limit):
                if a.text and len(a.text.split(" ")) > 3 and '\n' not in a.text:
                    ws.append(''.join(filter(lambda x: x in printable, a.text)))
            count = count + 1
    except (requests.ConnectionError):
        print ("ERROR. Invalid URL for WashingtonPost!")

    #############################
    # Call Sentimental Analysis #
    #############################
    ny_data, ny_alldata = analyze(ny)
    wp_data, ny_alldata = analyze(wp)
    fn_data, ny_alldata = analyze(fn)
    ws_data, ny_alldata = analyze(ws)

    ################
    # Write to CSV #
    ################
    size_list = [len(ny), len(wp), len(fn), len(ws)]
    size = max(size_list)
    for i in range(1, size):
        ny_article, wp_article, fn_article, ws_article = "", "", "", ""
        ny_article_data, wp_article_data, fn_article_data, ws_article_data = "", "", "", ""
        if i < len(ny):
            ny_article = ny[i]
        if i < len(wp):
            wp_article = wp[i]
        if i < len(fn):
            fn_article = fn[i]
        if i < len(ws):
            ws_article = ws[i]

        if i < len(ny_data):
            ny_article_data = ny_data[i]
        if i < len(wp_data):
            wp_article_data = wp_data[i]
        if i < len(fn_data):
            fn_article_data = fn_data[i]
        if i < len(ws_data):
            ws_article_data = ws_data[i]
        csv_writer.writerow(
            [ny_article, ny_article_data, wp_article, wp_article_data, fn_article, fn_article_data, ws_article, ws_article_data])

    csv_file.close()


start_time = time.time()
scrape()
print("--- %s seconds ---" % (time.time() - start_time))
