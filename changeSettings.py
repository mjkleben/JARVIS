import speech_recognition as sr
import os
import time
from gtts import gTTS  # Google text-to-speech

currentDirectory = os.path.dirname(__file__)
soundDirectory = currentDirectory + r"/sounds/"
setupPath = currentDirectory + "/setup/"  # USE AS GLOBAL VARIABLE
deviceLanguage = ""
with open(os.path.join(setupPath, "lang.txt"), "r") as readLang:
    deviceLanguage = readLang.readline()


def myCommand():
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
            command = self.myCommand()
    except Exception as e:
        pass

    print("You said: " + command.strip())

    return command.strip()


# ------------------------------------------------------------------------------------------------------------------------------------


def changeAccent():
    global deviceLanguage
    global currentDirectory
    global soundDirectory

    language = {"afrikaans": "af", "arabic": "ar", "bengali": "bn", "bosnian": "bs", "catalan": "ca", "czech": "cs", "welsh": "cy", "danish": "da", "german": "de", "greek": "el", "australian": "en-au", "canadian": "en-ca", "british": "en-gb", "irish": "en-ie", "indian": "en-ie", "united kingdom british": "en-uk", "english": "en", "finnish": "fi", "spain spanish": "es-es",
                "united states spanish": "es-us", "canadian french": "fr-ca", "french": "fr-fr", "hindi": "hi", "croatian": "hr", "hungarian": "hu", "armenian": "hy", "korean": "ko", "italian": "it", "japanese": "jw", "dutch": "nl", "norwegian": "no", "portuguese": "pt-br", "russian": "ru", "slovak": "sk", "thai": "th", "filipino": "tl", "turkish": "tr", "ukrainian": "uk", "vietnamese": "vi", "chinese": "zh-cn"}

    tts = gTTS("What would you like to change your language to?",
               lang=deviceLanguage)
    tts.save(os.path.join(soundDirectory, "WhichLanguage.mp3"))
    os.startfile(os.path.join(soundDirectory, "WhichLanguage.mp3"))

    answer = ""

    while answer not in language.keys():
        answer = myCommand().lower()
        if answer == "stop":
            break

    if answer in language.keys():
        print("YOUR ANSWER IS: " + answer)
        langAbbrev = language.get(answer)
        # CHANGE LANGUAGE
        deviceLanguage = langAbbrev
        langFilePath = currentDirectory + "\setup\\"  # USE AS GLOBAL VARIABLE
        with open(os.path.join(langFilePath, "lang.txt"), "w") as writeNewLang:
            writeNewLang.write(langAbbrev)

        tts = gTTS("Your language has been changed to " +
                   answer, lang=langAbbrev)
        tts.save(os.path.join(soundDirectory, "LanguageChanged.mp3"))
        os.startfile(os.path.join(soundDirectory, "LanguageChanged.mp3"))
    else:
        print("YOU STOPPED")
# ------------------------------------------------NAME CHANGER--------------------------------------------


def changeDeviceName():
    global deviceLanguage
    global currentDirectory
    global deviceName
    global soundDirectory
    print("NAME CHANGER")
    soundDirectory = currentDirectory + r"\sounds\\"

    tts = gTTS("What should my new name be?", lang=deviceLanguage)
    tts.save(os.path.join(soundDirectory, "NameQuestion.mp3"))
    os.startfile(os.path.join(soundDirectory, "NameQuestion.mp3"))

    time.sleep(2)

    deviceNameCopy = deviceName
    answer = deviceNameCopy
    while answer == deviceNameCopy:
        print("LOOP")
        answer = myCommand().lower()
        if answer == "stop":
            break
        elif answer == "":
            answer = deviceName
        elif answer == deviceName:
            tts = gTTS("That is already my name.", lang=deviceLanguage)
            tts.save(os.path.join(soundDirectory, "NameQuestion.mp3"))
            os.startfile(os.path.join(soundDirectory, "NameQuestion.mp3"))

    # rewrite the new name.
    newNameFilePath = currentDirectory + "\setup\\"  # USE AS GLOBAL VARIABLE
    with open(os.path.join(newNameFilePath, "device-name.txt"), "w") as writeNewName:
        writeNewName.write(answer)
    deviceName = answer

    tts = gTTS("Hi my name is " + answer +
               ". Happy to meet you", lang=deviceLanguage)
    tts.save(os.path.join(soundDirectory, "NewNameIntro.mp3"))
    os.startfile(os.path.join(soundDirectory, "NewNameIntro.mp3"))

    time.sleep(2)
