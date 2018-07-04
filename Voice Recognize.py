import speech_recognition as sr
import pyttsx3
import urllib.request, urllib.parse #for Youtube
import os, webbrowser,requests #for Google
import re
import requests
import bs4
from selenium import webdriver
from comtypes import *
import comtypes.client
from ctypes import POINTER
from ctypes.wintypes import DWORD, BOOL


currentDirectory = os.path.dirname(__file__)
chromedriverPath = currentDirectory + "\setup\chromedriver.exe"


#-------------------------------------VOLUME INCREASE, DECREASE--------------------------------------
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
            (['out','retval'], POINTER(c_float), 'pfLevelDB')
        ),
        COMMETHOD([], HRESULT, 'GetMasterVolumeLevelScalar',
            (['out','retval'], POINTER(c_float), 'pfLevelDB')
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
            (['out','retval'], POINTER(c_float), 'pfLevelDB')
        ),
        COMMETHOD([], HRESULT, 'GetChannelVolumeLevelScalar',
            (['in'], DWORD, 'nChannel'),
            (['out','retval'], POINTER(c_float), 'pfLevelDB')
        ),
        COMMETHOD([], HRESULT, 'SetMute',
            (['in'], BOOL, 'bMute'),
            (['in'], POINTER(GUID), 'pguidEventContext')
        ),
        COMMETHOD([], HRESULT, 'GetMute',
            (['out','retval'], POINTER(BOOL), 'pbMute')
        ),
        COMMETHOD([], HRESULT, 'GetVolumeStepInfo',
            (['out','retval'], POINTER(c_float), 'pnStep'),
            (['out','retval'], POINTER(c_float), 'pnStepCount'),
        ),
        COMMETHOD([], HRESULT, 'VolumeStepUp',
            (['in'], POINTER(GUID), 'pguidEventContext')
        ),
        COMMETHOD([], HRESULT, 'VolumeStepDown',
            (['in'], POINTER(GUID), 'pguidEventContext')
        ),
        COMMETHOD([], HRESULT, 'QueryHardwareSupport',
            (['out','retval'], POINTER(DWORD), 'pdwHardwareSupportMask')
        ),
        COMMETHOD([], HRESULT, 'GetVolumeRange',
            (['out','retval'], POINTER(c_float), 'pfMin'),
            (['out','retval'], POINTER(c_float), 'pfMax'),
            (['out','retval'], POINTER(c_float), 'pfIncr')
        ),

    ]

class IMMDevice(IUnknown):
    _iid_ = GUID('{D666063F-1587-4E43-81F1-B948E807363F}')
    _methods_ = [
        COMMETHOD([], HRESULT, 'Activate',
            (['in'], POINTER(GUID), 'iid'),
            (['in'], DWORD, 'dwClsCtx'),
            (['in'], POINTER(DWORD), 'pActivationParans'),
            (['out','retval'], POINTER(POINTER(IAudioEndpointVolume)), 'ppInterface')
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
            (['out','retval'], POINTER(POINTER(IMMDeviceCollection)), 'ppDevices')
        ),
        COMMETHOD([], HRESULT, 'GetDefaultAudioEndpoint',
            (['in'], DWORD, 'dataFlow'),
            (['in'], DWORD, 'role'),
            (['out','retval'], POINTER(POINTER(IMMDevice)), 'ppDevices')
        )
    ]

enumerator = comtypes.CoCreateInstance(
    CLSID_MMDeviceEnumerator,
    IMMDeviceEnumerator,
    comtypes.CLSCTX_INPROC_SERVER
)

endpoint = enumerator.GetDefaultAudioEndpoint( 0, 1 )
volume = endpoint.Activate( IID_IAudioEndpointVolume, comtypes.CLSCTX_INPROC_SERVER, None )

def myCommand():
    #Listen for command
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
        #loop back to continue to listen for commands if unrecognizable speech is received
        except sr.UnknownValueError:
            #print("UNKNOWN")
            print("in Except")
            command = myCommand();
    except Exception as e:
        pass

    return command.strip()
#------------------------YOUTUBER-----------------------------------------------

driver = webdriver.Chrome(chromedriverPath)
print(chromedriverPath)

def youtube(command):
    global driver
    global youtube_tab
    global youtube_open
    youtube_open = True

    try:
        os.system("taskkill /F /IM chrome.exe")
    except Exception as d:
        pass

    #If it's youtube instead of play
    vid = command
    if "youtube" == command[0:7]:
        vid = vid[7:]
    try:
        vid_search = vid

        query_string = urllib.parse.urlencode({"search_query": vid_search})
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())

        top_result = "http://www.youtube.com/watch?v=" + search_results[0]
        youtube_tab = top_result
        driver = webdriver.Chrome(chromedriverPath)
        driver.get(youtube_tab)

        print(youtube_tab)
        time.sleep(4)


    except Exception as e:
        os.startfile("error.mp3")


def stop():
    global youtube_open
    try:
        os.system("taskkill /F /IM chrome.exe")
        youtube_open = False
    except Exception as e:
        pass
#------------------------------------------------------------------------------------------
def computerMode(string):
    print("Computer mode")
    engine.say("Computer mode activated")
    engine.runAndWait()
    computerGoing = True
    while computerGoing:


        Message = ""
        # check that recognizer and microphone arguments are appropriate type
        if not isinstance(recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")
        if not isinstance(microphone, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance")
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=3, phrase_time_limit=10)

        try:
            print("TRYING")
            command = r.recognize_google(audio).lower().strip()
            print("YOUR COMPUTER COMMAND", command)
            db.child("My_SentMsg").set(command)

            if command[0:4] == "stop":
                computerGoing = False
            else:
                pass

        # loop back to continue to listen for commands if unrecognizable speech is received
        except sr.UnknownValueError:
            print("ERROR")
            pass
    engine.say("Computer mode stopped")
    engine.runAndWait()
    # print("UNKNOWN")


def googler(to_search_for): #opens a google page in a new window
    search = to_search_for

    try:
        print("Searching on Google...")

        #How many tabs should be open? Code
        how_many_tabs = 1
        list = []
        if not re.findall(r'\+\+(\w+)', search):
            print("Finding top result for " + "'" + search + "'"+ " ...")
        if re.findall(r'\+\+(\w+)', search):
            list = re.findall(r'\+\+(\w+)', search)
            if int(list[0]):
                how_many_tabs = int(list[0])
                search, separator, old_string = search.partition('++' + list[0])
                print("Finding top " + str(how_many_tabs) + " results for " + "'" + search + "'" + " ...")

        #Opening the tabs
        res = requests.get('https://google.com/search?q=' + search)
        soup = bs4.BeautifulSoup(res.text, 'lxml')
        links = soup.select('.r a')
        num_tabs = min(how_many_tabs, len(links))

        for i in range(num_tabs):
            webbrowser.open('https://google.com' + links[i].get('href'))



    except Exception as e:
        pass
#-----------------------JOKE-----------------------------------------------
def joke():
    res = requests.get(
        'https://icanhazdadjoke.com/',
        headers={"Accept": "application/json"}
    )
    if res.status_code == requests.codes.ok:
        print(str(res.json()['joke']))
        engine.say(str(res.json()['joke']))
        engine.runAndWait()
    else:
        engine.say('oops!I ran out of jokes')
        engine.runAndWait()
#--------------------------------------------------USING THE COMMANDS-----------------------------------
volumeLevel = int(volume.GetMasterVolumeLevel())
volume.SetMasterVolumeLevel(-10 ,None)
def assistant(command):
    global volumeLevel
    global youtube_open
    # print("-------------------------")
    # print("VOLUME LEVEL: ", volumeLevel)
    # print("---------------------------")
    #
    # print("UR COMMAND IS: ", command.strip())

    #Commands
    if "hey john" == command or "john" == command:
        stop()
        os.startfile("answer.mp3")
    elif "youtube" in command[0:7]:
        youtube(command)
    elif  "full screen" in command[0:12]:
        try:
            driver.implicitly_wait(20)
            driver.switch_to.frame(0)
            print(type(driver))
            element = driver.find_element_by_xpath("//button[@class='ytp-fullscreen-button ytp-button']")
            element.click()
        except:
            pass
    elif "pause" in command[0:5] or "play" in command[0:4]:
        try:
            driver.implicitly_wait(20)
            driver.switch_to.frame(0)
            print(type(driver))
            element = driver.find_element_by_xpath("//button[@class='ytp-play-button ytp-button']")
            element.click()
        except:
            pass
    elif "skip" in command[0:5]:
        try:
            driver.implicitly_wait(20)
            driver.switch_to.frame(0)
            print(type(driver))
            element = driver.find_element_by_xpath("//button[@class='videoAdUiSkipButton']")
            element.click()
        except:
            pass
    elif command == "stop":
        stop()

    elif "decrease volume" in command or "lower volume" in command:
        try:
            volume.SetMasterVolumeLevel(-20, None)
            engine.say("Volume decreased")
            engine.runAndWait()
        except:
            pass
    elif "increase volume" in command or "raise volume" in command:
        try:
            volume.SetMasterVolumeLevel(-3, None)
            print(volume.GetMasterVolumeLevel())
            engine.say("Volume increased")
            engine.runAndWait()
        except:
            pass
    elif command == "max volume":
        try:
            volume.SetMasterVolumeLevel(0, None)
            print(volume.GetMasterVolumeLevel())
            engine.say("Volume increased")
            engine.runAndWait()
        except:
            pass
    elif command =="mute" or command == "be quiet":
        try:
            volume.SetMasterVolumeLevel(-100, None)
            print(volume.GetMasterVolumeLevel())
            engine.say("Volume increased")
            engine.runAndWait()
        except:
            pass
    elif command == "mid volume":
        try:
            volume.SetMasterVolumeLevel(-10, None)
            print(volume.GetMasterVolumeLevel())
            engine.runAndWait()
        except:
            pass

    elif "google" in command[0:7]:
        googler(command[7:])

    elif command == "computer mode":
        computerMode(command)
    elif command == "goodbye john":
        sys.exit(0)
    elif 'joke' in command or "tell me a joke" in command:
        joke()
    elif command not in every_command and command != "":
        if youtube_open == False:
            pass
        else:
            pass
    else:
        pass
        #os.startfile("error.mp3")


#----------------Main function---------------------------------
#loop to continue executing multiple commands
recognizer = sr.Recognizer()
microphone = sr.Microphone()
engine = pyttsx3.init()
every_command = ["hey john", "john", "youtube", "google", "computer mode", "stop", "joke", "tell me a joke", "decrease volume", "lower volume", "increase volume", "raise volume"]

youtube_tab = ""
youtube_open = False
os.startfile(currentDirectory + "\sounds\start.mp3")
while True:
    assistant(myCommand())