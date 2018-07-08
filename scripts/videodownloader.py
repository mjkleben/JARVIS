from pytube import YouTube
import os

def video_downloader2(url): #downloads music given a youtube link
    print("HEYOOO                  " + url)
    try:
        desktop_path = str(os.path.join(os.environ['HOMEPATH'], 'Desktop'))
        #print(desktop_path)
        yt = YouTube(url.strip())
        print("SECOND STEP")
        yt.streams.first().download("C:" + desktop_path)

    except:
        print("Download failed. Check the link or try another link.")

link = ""

with open(os.path.dirname(__file__) + "\youtube_link.txt", "r") as file_reader:
    link = file_reader.readline()

video_downloader2(link)