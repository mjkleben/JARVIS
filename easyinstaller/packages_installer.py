import os

packages = ["SpeechRecognition", "youtube-dl", "urllib3", "selenium", "requests", "pytube", "bs4", "beautifulsoup4", "gtts", "comtypes", "ctypes", "gTTS"]

for package in packages:
    try:
        os.system("pip install " + package)
    except Exception as e:
        print(e)

input("-Press Enter to Exit-")