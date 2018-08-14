import pygame
import socket
import sys
import os
import subprocess

currentDirectory = os.path.dirname(__file__)
JARVISDirectory = currentDirectory + "/JARVIS.py"

pygame.init()

display_width = 1280
display_height = 800

gameDisplay = pygame.display.set_mode((display_width, display_height), pygame.FULLSCREEN)
pygame.display.set_caption("Jarvis")

black = (0, 0, 0)

clock = pygame.time.Clock()
crashed = False
jarvisImageOn = pygame.image.load(currentDirectory + '\images\jOnPygame.png')
jarvisImageOff = pygame.image.load(currentDirectory + '\images\jOffPygame.png')
blackBackground = pygame.image.load(currentDirectory + r'\images\black.png')

x = 390
y = 150
keep_going = True
gameDisplay.fill(black)


s = socket.socket()
host = socket.gethostname()
port = 6969
s.bind((host, port))

p = subprocess.Popen([sys.executable, JARVISDirectory], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

s.listen(5)
c = None

try:
   c, addr = s.accept()
   print('Got connection from', addr)
except Exception as e:
    print(e)


jarvisDisplay = True

while keep_going:
    animationAction = c.recv(1024).decode("utf-8")
    print(animationAction)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep_going = False

    if animationAction == "listening" and jarvisDisplay == True:
        gameDisplay.blit(jarvisImageOn, (x, y))
    elif animationAction == "trying" and jarvisDisplay == True:
        gameDisplay.blit(jarvisImageOff, (x, y))
    elif "goodbye" in animationAction:
        gameDisplay.blit(blackBackground, (x, y))
        jarvisDisplay = False
    elif "hi" in animationAction or "hey" in animationAction:
        gameDisplay.blit(jarvisImageOn, (x, y))
        jarvisDisplay = True


    pygame.display.update()
    clock.tick(5)

pygame.quit()
