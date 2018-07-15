from __future__ import unicode_literals
from pytube import YouTube
import os
import youtube_dl


def video_downloader2(FILLER_URL): #downloads music given a youtube link
    try:
        desktop_path = str(os.path.join(os.environ['HOMEPATH'], 'Desktop'))
        #print(desktop_path)
        yt = YouTube(FILLER_URL)
        yt.streams.first().download("C:" + desktop_path)

    except:
        print("Download failed. Check the link or try another link.")


options = {
  'format': 'bestaudio/best',
  'extractaudio' : True,  # only keep the audio
  'audioformat' : "mp3",  # convert to mp3
  'outtmpl': '%(id)s',    # name the file the ID of the video
  'noplaylist' : True,    # only download single song, not playlist
}

with youtube_dl.YoutubeDL(options) as ydl:
    ydl.download(['https://www.youtube.com/watch?v=rAsI0qVZihQ'])