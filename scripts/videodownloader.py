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

video_downloader2("https://www.youtube.com/watch?v=BdsdgL4_wuY")