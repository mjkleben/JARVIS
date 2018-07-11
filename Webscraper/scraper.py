from bs4 import BeautifulSoup
import requests
import csv


def scrape():
    csv_file = open('news.csv', 'w')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['NYTimes', 'WashingtonPost',
                         'CNN', 'FoxNews', 'WallStreet'])
    ny = [""]
    wp = [""]
    cn = [""]
    fn = [""]
    ws = [""]
    # New York Times #
    try:
        source = requests.get("https://www.nytimes.com/").text
        soup = BeautifulSoup(source, 'lxml')
        for article in soup.find_all('article'):
            for header in article.find_all('a'):
                if(header.text and 'Comments' not in header.text and '\n' not in header.text):
                    ny.append(header.text)
    except (requests.ConnectionError):
        print ("ERROR. Invalid URL for NYTimes!")
    # Washington Post #
    try:
        source = requests.get(
            "https://www.washingtonpost.com/?noredirect=on").text
        soup = BeautifulSoup(source, 'lxml').find(
            'section', id='main-content')
        headlines = soup.find_all('div', class_='headline')
        for headline in headlines:
            wp.append(headline.a.text)
    except (requests.ConnectionError):
        print ("ERROR. Invalid URL for WashingtonPost!")

    # # CNN #
    # try:
    #     source = requests.get(
    #         "https://www.cnn.com/").text
    #     soup = BeautifulSoup(source, 'lxml').find(
    #         'div', class_='pg-no-rail pg-wrapper ')
    #     for span in soup.find_all('span'):
    #         print(span.prettify())

    #     # headlines = soup.find_all('div', class_='headline')
    #     # for headline in headlines:
    #     #     wp.append(headline.a.text)
    # except (requests.ConnectionError):
    #     print ("ERROR. Invalid URL for WashingtonPost!")
    # # Fox News #
    # # Wall Street #
    list = [len(ny), len(wp), len(cn), len(fn), len(ws)]
    size = max(list)
    for i in range(1, size):
        ny_article, wp_article, cn_article, fn_article, ws_article = "", "", "", "", ""
        if i < len(ny):
            ny_article = ny[i]
        if i < len(wp):
            wp_article = wp[i]
        if i < len(cn):
            cn_article = cn[i]
        if i < len(fn):
            fn_article = fn[i]
        if i < len(ws):
            ws_article = ws[i]
        csv_writer.writerow(
            [ny_article, wp_article, cn_article, fn_article, ws_article])

    csv_file.close()


scrape()

# for article in soup.find_all('article'):
#     try:
#         vid_src = article.find(
#             'iframe', class_='youtube-player')['src']
#         vid_id = vid_src.split('/')[4].split('?')[0]
#         yt_link = f'https://youtube.com/watch?v={vid_id}'
#     except expression as identifier:
#         yt_link = "No Youtube Link!"
#     print (yt_link)
#     csv_writer.writerow([yt_link])
