import speech_recognition as sr
import os
import webbrowser
import re
import requests
import bs4
from selenium import webdriver
from ctypes import POINTER
import threading
import pygame
from gtts import gTTS  # Google text-to-speech
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pickle

try:
    from comtypes import *
    import comtypes.client
    from ctypes.wintypes import DWORD, BOOL
except Exception as e:
    print("These modules are not supported by the operating system.")

# Custom modules
from changeSettings import changeAccent, changeDeviceName
from YouTubeCommands import youtube, YouTubeToMp3, downloadYouTube, YouTubeCommands
from mp3Player import playMp3
from Google import googler
import AnimationAction

# Setting up the Chrome Selenium Webdriver and getting PATHs setup for easy access later with "global"
currentDirectory = os.path.dirname(__file__)
soundDirectory = currentDirectory + r"/sounds//"
chromedriverPath = currentDirectory + "/setup/chromedriver.exe"
setupPath = currentDirectory + "\setup\\"  # USE AS GLOBAL VARIABLE

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chromedriverPath, chrome_options=chrome_options)
driver.close()

# Start mp3 player
pygame.mixer.init()
AnimationAction.init()

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
    # Listen for command
    command = ""
    try:
        r = sr.Recognizer()
        print("Listening for command")

        with sr.Microphone() as source:
            r.pause_threshold = 0.5
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=3, phrase_time_limit=10)

        try:
            print("trying")

            command = r.recognize_google(audio).lower()

            print("after trying")
        # loop back to continue to listen for commands if unrecognizable speech is received
        except sr.UnknownValueError:
            # print("UNKNOWN")
            print("in Except")
            command = myCommand()
    except Exception as e:
        pass

    print("You said: " + command.strip())

    return command.strip()
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
    # Basically stops every process going in on chrome

    # Should make youtube_tab nothing because we stopped Chrome
    global youtube_tab
    youtube_tab = ""

    try:
        os.system("taskkill /F /IM chrome.exe")
        youtube_open = False
    except Exception as e:
        pass


# --------------------------------------------------USING THE COMMANDS-----------------------------------
# Set the current volume to medium volume
volumeLevel = int(volume.GetMasterVolumeLevel())
volume.SetMasterVolumeLevel(-10, None)


def assistant(command):
    global volumeLevel
    global youtube_open
    global youtube_tab
    global deviceName
    global currentDirectory
    global driver

    # Commands
    if command == "hey " + deviceName or command == deviceName:
        stop()
        playMp3(currentDirectory + r"\sounds\answer.mp3")
    elif command == "change voice" or command == "change accent":
        changeAccent()
    elif command == "change name" or command == "name change":
        changeDeviceName()
    elif command[0:4] == "open":
        openApp(command[4:])
    elif ("youtube" in command[0:7]) and ("search youtube" not in command) and ("youtube search" not in command):
        youtube(command)
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
    elif command in youtube_commands:
        YouTubeCommands(command)
    elif command == "download video":
        downloadYouTube(youtube_tab)

    elif command == "download music":
        download_thread = threading.Thread(target=YouTubeToMp3, args=())
        download_thread.start()
    elif command == "stop":
        stop()
    elif "google" in command[0:7]:
        googler(command[7:])
    elif command == "goodbye " + deviceName:
        exit(0)
    elif 'joke' in command or "tell me a joke" in command:
        joke()
    elif command not in every_command and command != "":
        if youtube_open == False:
            pass
        else:
            pass
    # -------------------------------------------------------------VOLUME SETTINGS
    elif "decrease volume" in command or "lower volume" in command:
        try:
            volume.SetMasterVolumeLevel(-20, None)
            # engine.say("Volume decreased")
            # engine.runAndWait()
        except:
            pass
    elif "increase volume" in command or "raise volume" in command:
        try:
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
#playMp3(currentDirectory + "\sounds\start.mp3")
while True:
    assistant(myCommand())
