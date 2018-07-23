import pygame

def playMp3(mp3File):
    pygame.mixer.music.load(mp3File)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue