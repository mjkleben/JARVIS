import pygame
import socket
import sys
import os
import subprocess
from tkinter import Tk
import time
import pygame.font


#Setting the display for pygame
pygame.init()
display_width = 1280
display_height = 800
# gameDisplay = pygame.display.set_mode((display_width, display_height), pygame.FULLSCREEN)
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Jarvis")
x = 390
y = 150


#Directories
currentDirectory = os.path.dirname(__file__)
setupDirectory = currentDirectory + "/setup/"
JARVISDirectory = currentDirectory + "/JARVIS.py"
jarvisImageOn = pygame.image.load(currentDirectory + '\images\jarvisOn1.png').convert_alpha()
jarvisImageOff = pygame.image.load(currentDirectory + '\images\jarvisOff1.png').convert_alpha()
background = pygame.image.load(currentDirectory + r'\images\black.png')
jarvisImageOn2 = pygame.image.load(currentDirectory + '\images\jarvisOn2.png').convert_alpha()
jarvisImageOff2 = pygame.image.load(currentDirectory + '\images\jarvisOff2.png').convert_alpha()
background2 = pygame.image.load(currentDirectory + r'\images\silver.png')


#Color of background
black = (0, 0, 0)
silver = (233,232,232)
currentDesignColor = ""
with open(os.path.join(setupDirectory, "color-scheme.txt"), "r") as color:
    currentDesignColor = color.readline()
if currentDesignColor == "dark":
    gameDisplay.fill(black)
if currentDesignColor == "light":
    gameDisplay.fill(silver)
clock = pygame.time.Clock()



#Connecting to main Jarvis
s = socket.socket()
host = socket.gethostname()
port = 6969
s.bind((host, port))
p = subprocess.Popen([sys.executable, JARVISDirectory], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

s.listen(5)
c = None
# root = Tk()

try:
   c, addr = s.accept()
   print('Got connection from', addr)
except Exception as e:
    print(e)


# text_font = pygame.font.SysFont("comic Sans MS", 30)
#
# def screen_message(msg):
#     text = text_font.render(msg, False, (0, 0, 0))
#     gameDisplay.blit(text, (0, 0))

#Important Boolean Values
keep_going = True
jarvisDisplay = True

while keep_going:
    # root.wm_attributes("-topmost", 1)
    animationAction = c.recv(1024).decode("utf-8")
    print(animationAction)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep_going = False

    temporaryColor = ""
    if currentDesignColor == "dark":
        if animationAction == "listening" and jarvisDisplay == True:
            gameDisplay.blit(jarvisImageOn, (x, y))
        elif animationAction == "trying" and jarvisDisplay == True:
            gameDisplay.blit(jarvisImageOff, (x, y))
        if ("change" in animationAction) and ("design" in animationAction):
            print("CHANGED")
            with open(os.path.join(setupDirectory, "color-scheme.txt"), "w") as newColor:
                newColor.write("light")
            currentDesignColor = "light"
            gameDisplay.fill(silver)
        elif "goodbye" in animationAction:
            gameDisplay.blit(background, (x, y))
            jarvisDisplay = False
        elif "hi" in animationAction or "hey" in animationAction:
            gameDisplay.blit(jarvisImageOn, (x, y))
            jarvisDisplay = True

    elif currentDesignColor == "light":
        if animationAction == "listening" and jarvisDisplay == True:
            gameDisplay.blit(jarvisImageOn2, (x, y))
        elif animationAction == "trying" and jarvisDisplay == True:
            gameDisplay.blit(jarvisImageOff2, (x, y))
        if ("change" in animationAction) and ("design" in animationAction):
            with open(os.path.join(setupDirectory, "color-scheme.txt"), "w") as newColor:
                newColor.write("dark")
            currentDesignColor = "dark"
            gameDisplay.fill(black)
        elif "goodbye" in animationAction:
            gameDisplay.blit(background2, (x, y))
            jarvisDisplay = False
        elif "hi" in animationAction or "hey" in animationAction:
            gameDisplay.blit(jarvisImageOn2, (x, y))
            jarvisDisplay = True
    # if animationAction != "" and animationAction != "listening" and animationAction != "trying":
    #     screen_message(animationAction)
    #
    #
    # time.sleep(2)
    #
    # pygame.draw.rect(gameDisplay, (255,255,255), (0, 0, 500, 200))

    # currentDesignColor = temporaryColor
    pygame.display.update()
    clock.tick(5)
    # root.wm_attributes("-topmost", 1)
    print(currentDesignColor)

pygame.quit()
