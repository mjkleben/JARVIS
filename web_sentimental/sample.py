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
# list = ["Hello my name", "is Sung Joon"]
# for sentence in list:
#     for word in sentence.split(" "):
#         print(word)
# string = list("~!@#$%^&*()_-+=1234567890{}[]\|?/><,.;:")
# print(string)

# import datetime
import os

word = "hello my name is sung joon"
info = os.popen("curl -d"+" 'text="+word+"' " +
                "http://text-processing.com/api/sentiment/").read()
print info
