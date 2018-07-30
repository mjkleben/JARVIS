import speech_recognition as sr
import os
import re
import requests
from ctypes import POINTER
import threading
import pygame
from gtts import gTTS  # Google text-to-speech
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import socket
import urllib.request
import urllib.parse  # for Youtube
from pytube import YouTube  # for downloading YouTube videos
import bs4

try:
    from comtypes import *
    import comtypes.client
    from ctypes.wintypes import DWORD, BOOL
except Exception as e:
    print("These modules are not supported by the operating system.")

# Custom modules
from changeSettings import changeAccent, changeDeviceName
# from YouTubeCommands import youtube, YouTubeToMp3, downloadYouTube, YouTubeCommands
from mp3Player import playMp3
# from Google import googler

# Setting up the Chrome Selenium Webdriver and getting PATHs setup for easy access later with "global"
currentDirectory = os.path.dirname(__file__)
soundDirectory = currentDirectory + r"/sounds//"
chromedriverPath = currentDirectory + "/setup/chromedriver"
setupPath = currentDirectory + "/setup/"  # USE AS GLOBAL VARIABLE

#Set up Chrome Driver
# chrome_options = Options()
# chrome_options.add_argument("--headless")
# driver = webdriver.Chrome(chromedriverPath, chrome_options=chrome_options)
# driver.close()
driver = None

#Variables for scrolling up or down
scroll_num = 0
scroll = str(270)

# Start mp3 player
pygame.mixer.init()


#driver closen? variable to see whether new driver has to be made
driverClosen = False

# Connect to the Animation
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 6969
# print(host)
s.connect((host, port))
print ('Connected to', host)
# -------------------------------------Volume Control Setup--------------------------------------
try:
    MMDeviceApiLib = \
        GUID('{2FDAAFA3-7523-4F66-9957-9D5E7FE698F6}')
    IID_IMMDevice = \
        GUID('{D666063F-1587-4E43-81F1-B948E807363F}')
    IID_IMMDeviceEnumerator = \
        GUID('{A95664D2-9614-4F35-A746-DE8DB63617E6}')
    CLSID_MMDeviceEnumerator = \
        GUID('{BCDE0395-E52F-467C-8E3D-C4579291692E}')
    IID_IMMDeviceCollection = \
        GUID('{0BD7A1BE-7A1A-44DB-8397-CC5392387B5E}')
    IID_IAudioEndpointVolume = \
        GUID('{5CDF2C82-841E-4546-9722-0CF74078229A}')

    class IMMDeviceCollection(IUnknown):
        _iid_ = GUID('{0BD7A1BE-7A1A-44DB-8397-CC5392387B5E}')
        pass

    class IAudioEndpointVolume(IUnknown):
        _iid_ = GUID('{5CDF2C82-841E-4546-9722-0CF74078229A}')
        _methods_ = [
            STDMETHOD(HRESULT, 'RegisterControlChangeNotify', []),
            STDMETHOD(HRESULT, 'UnregisterControlChangeNotify', []),
            STDMETHOD(HRESULT, 'GetChannelCount', []),
            COMMETHOD([], HRESULT, 'SetMasterVolumeLevel',
                      (['in'], c_float, 'fLevelDB'),
                      (['in'], POINTER(GUID), 'pguidEventContext')
                      ),
            COMMETHOD([], HRESULT, 'SetMasterVolumeLevelScalar',
                      (['in'], c_float, 'fLevelDB'),
                      (['in'], POINTER(GUID), 'pguidEventContext')
                      ),
            COMMETHOD([], HRESULT, 'GetMasterVolumeLevel',
                      (['out', 'retval'], POINTER(c_float), 'pfLevelDB')
                      ),
            COMMETHOD([], HRESULT, 'GetMasterVolumeLevelScalar',
                      (['out', 'retval'], POINTER(c_float), 'pfLevelDB')
                      ),
            COMMETHOD([], HRESULT, 'SetChannelVolumeLevel',
                      (['in'], DWORD, 'nChannel'),
                      (['in'], c_float, 'fLevelDB'),
                      (['in'], POINTER(GUID), 'pguidEventContext')
                      ),
            COMMETHOD([], HRESULT, 'SetChannelVolumeLevelScalar',
                      (['in'], DWORD, 'nChannel'),
                      (['in'], c_float, 'fLevelDB'),
                      (['in'], POINTER(GUID), 'pguidEventContext')
                      ),
            COMMETHOD([], HRESULT, 'GetChannelVolumeLevel',
                      (['in'], DWORD, 'nChannel'),
                      (['out', 'retval'], POINTER(c_float), 'pfLevelDB')
                      ),
            COMMETHOD([], HRESULT, 'GetChannelVolumeLevelScalar',
                      (['in'], DWORD, 'nChannel'),
                      (['out', 'retval'], POINTER(c_float), 'pfLevelDB')
                      ),
            COMMETHOD([], HRESULT, 'SetMute',
                      (['in'], BOOL, 'bMute'),
                      (['in'], POINTER(GUID), 'pguidEventContext')
                      ),
            COMMETHOD([], HRESULT, 'GetMute',
                      (['out', 'retval'], POINTER(BOOL), 'pbMute')
                      ),
            COMMETHOD([], HRESULT, 'GetVolumeStepInfo',
                      (['out', 'retval'], POINTER(c_float), 'pnStep'),
                      (['out', 'retval'], POINTER(c_float), 'pnStepCount'),
                      ),
            COMMETHOD([], HRESULT, 'VolumeStepUp',
                      (['in'], POINTER(GUID), 'pguidEventContext')
                      ),
            COMMETHOD([], HRESULT, 'VolumeStepDown',
                      (['in'], POINTER(GUID), 'pguidEventContext')
                      ),
            COMMETHOD([], HRESULT, 'QueryHardwareSupport',
                      (['out', 'retval'], POINTER(DWORD), 'pdwHardwareSupportMask')
                      ),
            COMMETHOD([], HRESULT, 'GetVolumeRange',
                      (['out', 'retval'], POINTER(c_float), 'pfMin'),
                      (['out', 'retval'], POINTER(c_float), 'pfMax'),
                      (['out', 'retval'], POINTER(c_float), 'pfIncr')
                      ),
        ]

    class IMMDevice(IUnknown):
        _iid_ = GUID('{D666063F-1587-4E43-81F1-B948E807363F}')
        _methods_ = [
            COMMETHOD([], HRESULT, 'Activate',
                      (['in'], POINTER(GUID), 'iid'),
                      (['in'], DWORD, 'dwClsCtx'),
                      (['in'], POINTER(DWORD), 'pActivationParans'),
                      (['out', 'retval'], POINTER(
                          POINTER(IAudioEndpointVolume)), 'ppInterface')
                      ),
            STDMETHOD(HRESULT, 'OpenPropertyStore', []),
            STDMETHOD(HRESULT, 'GetId', []),
            STDMETHOD(HRESULT, 'GetState', [])
        ]
        pass

    class IMMDeviceEnumerator(comtypes.IUnknown):
        _iid_ = GUID('{A95664D2-9614-4F35-A746-DE8DB63617E6}')

        _methods_ = [
            COMMETHOD([], HRESULT, 'EnumAudioEndpoints',
                      (['in'], DWORD, 'dataFlow'),
                      (['in'], DWORD, 'dwStateMask'),
                      (['out', 'retval'], POINTER(
                          POINTER(IMMDeviceCollection)), 'ppDevices')
                      ),
            COMMETHOD([], HRESULT, 'GetDefaultAudioEndpoint',
                      (['in'], DWORD, 'dataFlow'),
                      (['in'], DWORD, 'role'),
                      (['out', 'retval'], POINTER(POINTER(IMMDevice)), 'ppDevices')
                      )
        ]
    enumerator = comtypes.CoCreateInstance(
        CLSID_MMDeviceEnumerator,
        IMMDeviceEnumerator,
        comtypes.CLSCTX_INPROC_SERVER
    )
    endpoint = enumerator.GetDefaultAudioEndpoint(0, 1)
    volume = endpoint.Activate(IID_IAudioEndpointVolume,
                               comtypes.CLSCTX_INPROC_SERVER, None)
except Exception as e:
    print(e)
    print("Volume increase/decrease does not work with this OS")
# ------------------------------------GETTING USER VOICE COMMAND, the Voice Recognition Part------------------------


def myCommand():
    global currentDirectory
    global s
    # Listen for command
    command = ""
    try:
        r = sr.Recognizer()
        print("Listening for command")
        s.sendall("listening".encode("utf-8"))

        with sr.Microphone() as source:
            r.pause_threshold = 0.5
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=3, phrase_time_limit=10)

        try:
            print("trying")
            s.sendall("trying".encode("utf-8"))

            command = r.recognize_google(audio).lower()

            print("after trying")
        # loop back to continue to listen for commands if unrecognizable speech is received
        except sr.UnknownValueError:
            # print("UNKNOWN")
            print("in Except")
            command = myCommand()
    except Exception as e:
        pass
    #
    # s.sendall(command.encode("utf-8"))

    print(("You said: " + command))
    return command.strip()

def incognitoMode():
    global chromedriverPath
    global driver

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--incognito")

    driver = webdriver.Chrome(chromedriverPath, chrome_options=chrome_options)

# -----------------------Joke Teller-----------------------------------------------


def joke():
    global deviceLanguage
    global soundDirectory

    res = requests.get(
        'https://icanhazdadjoke.com/',
        headers={"Accept": "application/json"}
    )
    if res.status_code == requests.codes.ok:
        print(str(res.json()['joke']))
        tts = gTTS(str(res.json()['joke']), deviceLanguage)
        tts.save(os.path.join(soundDirectory, "joke.mp3"))
        playMp3(os.path.join(soundDirectory, "joke.mp3"))

    else:
        # engine.say('oops!I ran out of jokes')
        # engine.runAndWait()
        pass

# ----------------------------------Opens Apps in the MyApplications folder---------------------


def openApp(appName):
    appName = appName.strip()
    global currentDirectory
    print(os.listdir(currentDirectory))
    list = os.listdir(currentDirectory)

    regexp = re.compile(appName)

    for app in list:
        app = app.lower()
        print(app)
        if appName in app:
            os.startfile(currentDirectory + r"\MyApplications\\" + app)
            break

# ----------------------------------------Kill all current Chrome tabs/windows----------------------------
def stop():
    global driver
    global chromedriverPath
    global driverClosen
    if driver == None:
        driver = webdriver.Chrome(chromedriverPath)
    # Basically stops every process going in on chrome

    # Should make youtube_tab nothing because we stopped Chrome

    try:
        driver.close()
        driverClosen = True
        youtube_open = False
    except Exception as e:
        pass


# --------------------------------------------------USING THE COMMANDS-----------------------------------
# -------------------------------------YouTube and its commands-------------------------------
def youtube(command):
    global youtube_tab
    global youtube_open
    global driver
    global chromedriverPath
    global driverClosen

    if driver == None:
        driver = webdriver.Chrome(chromedriverPath)
    if driverClosen == True:
        driver = driver = webdriver.Chrome(chromedriverPath)
        driverClosen = False


    youtube_open = True

    # If it's youtube instead of play
    vid = command
    if "youtube" == command[0:7]:
        vid = vid[7:]
    try:
        vid_search = vid

        query_string = urllib.parse.urlencode({"search_query": vid_search})
        html_content = urllib.request.urlopen(
            "http://www.youtube.com/results?" + query_string)
        search_results = re.findall(
            r'href=\"\/watch\?v=(.{11})', html_content.read().decode())

        top_result = "http://www.youtube.com/watch?v=" + search_results[0]
        youtube_tab = top_result
        driver.get(youtube_tab)

        youtubeLinkFile = currentDirectory + "\scripts"

        with open(os.path.join(youtubeLinkFile, "youtube_link.txt"), "w") as write_tab:
            write_tab.write(youtube_tab)

    except Exception as e:
        print(e)
        # os.startfile("error.mp3")


def YouTubeToMp3():
    musicdownloader_path = currentDirectory + "\scripts\musicdownloader.py"
    os.system("python " + musicdownloader_path)


def downloadYouTube(url):
    try:
        desktop_path = str(os.path.join(os.environ['HOMEPATH'], 'Desktop'))
        # print(desktop_path)
        yt = YouTube(url.strip())
        print("SECOND STEP")
        yt.streams.first().download("C:" + desktop_path)

    except:
        print("Download failed. Check the link or try another link.")


def YouTubeCommands(command):
    global driver
    global chromedriverPath
    if driver == None:
        driver = webdriver.Chrome(chromedriverPath)

    print("IN YOUTUBE COMMANDS")
    if "full screen" in command:
        try:
            classname = 'button.ytp-fullscreen-button'
            button = driver.find_element_by_css_selector(classname).click()
        except Exception as e:
            print(e)
    elif "play" in command or "pause" in command:
        try:
            classname = 'button.ytp-play-button'
            button = driver.find_element_by_css_selector(classname).click()
        except Exception as e:
            print(e)
    elif "skip" in command or "skip video" in command:
        try:
            element = driver.find_element_by_css_selector("a.ytp-next-button")
            element.click()
        except Exception as f:
            print(f)
    elif "search youtube" == command[14:] or "youtube search" == command[14:]:
        try:
            element = driver.find_element_by_id("search")
            element.send_keys(command[14:])
            element.send_keys(u'\ue007')
        except Exception as f0:
            print(f0)

# -------------------------------Googler---------------------------------------
def googler(to_search_for):  # opens a google page in a new window
    global driver
    global chromedriverPath
    if driver == None:
        driver = webdriver.Chrome(chromedriverPath)
    search = to_search_for

    try:
        print("Searching on Google...")

        # How many tabs should be open? Code
        how_many_tabs = 1
        list = []
        if not re.findall(r'\+\+(\w+)', search):
            print("Finding top result for " + "'" + search + "'" + " ...")
        if re.findall(r'\+\+(\w+)', search):
            list = re.findall(r'\+\+(\w+)', search)
            if int(list[0]):
                how_many_tabs = int(list[0])
                search, separator, old_string = search.partition(
                    '++' + list[0])
                print("Finding top " + str(how_many_tabs) +
                      " results for " + "'" + search + "'" + " ...")

        # Opening the tabs
        res = requests.get('https://google.com/search?q=' + search)
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        links = soup.select('.r a')
        num_tabs = min(how_many_tabs, len(links))

        for i in range(num_tabs):
            driver.get('https://google.com' + links[i].get('href'))

    except Exception as e:
        print(e)


#-------------------------------------VOLUME STUFF----------
# Set the current volume to medium volume
try:
    volumeLevel = int(volume.GetMasterVolumeLevel())
    volume.SetMasterVolumeLevel(-10, None)
except:
    print("Volume control is not supported by this OS")

def assistant(command):
    global volumeLevel
    global youtube_open
    global youtube_tab
    global deviceName
    global currentDirectory
    global driver
    global scroll
    global scroll_num


    #ROOT COMMAND
    if command == "hey " + deviceName or command == deviceName:
        stop()
        playMp3(currentDirectory + r"\sounds\answer.mp3")

    #Internet Commands
    elif "incognito" == command or "incognito mode" == command:
        incognitoMode()
    elif "click" in command:
        try:
            link = driver.find_element_by_link_text(command[5:].strip().upper())
            link.click()
        except Exception as e:
            print(e)
        try:
            link = driver.find_element_by_link_text(command[5:].strip().lower())
            link.click()
        except Exception as e:
            print(e)
        try:
            link = driver.find_element_by_link_text(command[5:].strip().capitalize())
            link.click()
        except Exception as e:
            print(e)

    elif command == "go back":
        driver.back()
    elif command == "go forward":
        driver.forward()
    elif "refresh" in command:
        driver.refresh()
    elif command == "scroll down":
        try:
            driver.execute_script("window.scrollTo(0, " + scroll + ");")
        except Exception as e:
            print(e)
        scroll_num += 370
        scroll = str(scroll_num)
    elif command == "scroll up":
        if scroll_num > 370:
            scroll_num -= 370
            scroll = str(scroll_num)
        try:
            print("window.scrollTo(0, " + scroll + ");")
            driver.execute_script("window.scrollTo(0, " + scroll + ");")
        except Exception as e:
            print(e)

    elif command == "minimize window":
        try:
            driver.set_window_position(-10000, 0)
        except:
            pass
    elif command == "maximize window":
        try:
            driver.maximize_window()
        except:
            pass


        #Internet--YouTube
    elif ("youtube" in command[0:7]) and ("search youtube" not in command) and ("youtube search" not in command):
        youtube(command)
    elif command in youtube_commands:
        YouTubeCommands(command)
    elif command == "download video":
        downloadYouTube(youtube_tab)
    elif command == "download music":
        download_thread = threading.Thread(target=YouTubeToMp3, args=())
        download_thread.start()



    #Setting Commands
    elif command == "change voice" or command == "change accent":
        changeAccent()
    elif command == "change name" or command == "name change":
        changeDeviceName()
    elif command[0:4] == "open":
        openApp(command[4:])



    #Joke Teller
    elif 'joke' in command or "tell me a joke" in command:
        joke()

    elif command == "stop":
        stop()
    elif "google" in command[0:7]:
        googler(command[7:])
    elif command == "goodbye " + deviceName:
        exit(0)

    #Computer Commands
    elif "sleep" in command:
        print("YEET")
        try:
            os.system("shutdown.exe /h")
        except Exception as e:
            print(e)
    elif "decrease volume" in command or "lower volume" in command:
        try:
            volume.SetMasterVolumeLevel(-20, None)
            # engine.say("Volume decreased")
            # engine.runAndWait()
        except:
            pass
    elif "increase volume" in command or "raise volume" in command:
        try:
            print("Vol increased")
            volume.SetMasterVolumeLevel(-3, None)
            print(volume.GetMasterVolumeLevel())
            # engine.say("Volume increased")
            # engine.runAndWait()
        except:
            pass
    elif command == "max volume":
        try:
            volume.SetMasterVolumeLevel(0, None)
            print(volume.GetMasterVolumeLevel())
            # engine.say("Volume increased")
            # engine.runAndWait()
        except:
            pass
    elif command == "mute" or command == "be quiet":
        try:
            volume.SetMasterVolumeLevel(-100, None)
            print(volume.GetMasterVolumeLevel())
            # engine.say("Volume increased")
            # engine.runAndWait()
        except:
            pass
    elif command == "mid volume":
        try:
            volume.SetMasterVolumeLevel(-10, None)
            print(volume.GetMasterVolumeLevel())
            # engine.runAndWait()
        except:
            pass
    else:
        pass
        # os.startfile("error.mp3")


# ----------------Main function---------------------------------
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Use the every_command list for later, not in use at the moment
every_command = ["youtube", "google", "computer mode", "stop", "joke", "tell me a joke",
                 "decrease volume", "lower volume", "increase volume", "raise volume"]
youtube_commands = ["full screen", "play", "pause", "skip", "skip video"]


deviceLanguage = ""

with open(os.path.join(setupPath, "lang.txt"), "r") as readLang:
    deviceLanguage = readLang.readline()

# SETUP NAME
deviceName = ""
with open(os.path.join(setupPath, "device-name.txt"), "r") as readLang:
    deviceName = readLang.readline()
every_command.append(deviceName)

# For later use
youtube_tab = ""
youtube_open = False

# ----------------------------------------------------------------------PROGRAM STARTS HERE
# Basically the main function
#playMp3(currentDirectory + "/sounds/start.mp3")
while True:
    assistant(myCommand())
