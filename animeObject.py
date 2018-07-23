import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QMenu, QDesktopWidget
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QPixmap, QRegion
from time import sleep

def set_maid(n):
    pic = QPixmap(n)  # Get Maid
    maid.resize(pic.width(), pic.height())  # Resize the container
    maid.move(0, 200 - pic.height())  # Keep Maid at bottom > 800
    maid.setPixmap(pic)


class Animation(QThread):
    def __init__(self):
        self.animationCommand = ""

    def __str__(self):
        return self.animationCommand

    def change(self, command):
        assert isinstance(command, str)
        self.animationCommand = command

    def not_now(self):

        while 1 > 0:
            switch = "off"
            for i in range(1, 16):
                print('ball ' + str(i))
                # switch = input("Enter: ")
                if self.animationCommand == "listening":
                    set_maid("jOn.png")
                # sleep(1 / 54)
                # if i == 15:
                #     print('ok')
                #     sleep((1 / 35) * 10)

    def fps():
        print("Getting Ready.")
        for i in range(10, 30):
            fps = i
            count = 0
            print('fps: ' + str(i))
            while count < 10:
                set_maid(1)
                sleep(1 / fps)
                set_maid("maid")
                sleep(1 / fps)
                count += 1
            print("We're ready!")

    def run(self):
        print("Getting Ready.")
        sleep(1)
        self.not_now()
