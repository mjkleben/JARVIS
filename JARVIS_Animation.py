import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QMenu, QDesktopWidget
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QPixmap, QRegion
from time import sleep
import socket
import subprocess
import time

currentDirectory = os.path.dirname(__file__)
s = socket.socket()
host = socket.gethostname()
port = 6969
s.bind((host, port))


currentDirectory = os.path.dirname(__file__)
JARVISDirectory = currentDirectory + "/JARVIS.py"
p = subprocess.Popen([sys.executable, JARVISDirectory], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

s.listen(5)
c = None

try:
   c, addr = s.accept()
   print('Got connection from', addr)
except Exception as e:
    print(e)

def set_maid(n):
    pic = QPixmap(n)  # Get Maid
    maid.resize(pic.width(), pic.height())  # Resize the container
    maid.move(0, 262 - pic.height())  # Keep Maid at bottom > 800
    maid.setPixmap(pic)


class Animation(QThread):
    def not_now(self):
        global currentDirectory
        global c
        global addr
        animationAction = ""
        hidden = False

        while True:
            placeholder = animationAction

            while animationAction == placeholder:
                animationAction = c.recv(1024).decode("utf-8")

            # input("FINALLY")
            # print(animationAction)
            # input("New action")
            print(animationAction)
            if hidden == False:
                if animationAction == "listening":
                    set_maid("jOn.png")

                if animationAction == "trying":
                    set_maid("jOff.png")
            if animationAction == "hide":
                hidden = True
                set_maid("background.png")

            if animationAction == "unhide":
                hidden = False
        print("ok")
    def run(self):
        print("Getting Ready.")
        sleep(1)
        self.not_now()


class Window(QWidget):
    def __init__(self, parent=None):
        global maid

        QWidget.__init__(self, parent)
        self.setGeometry(0, 0, 800, 800)
        screen = QDesktopWidget().availableGeometry()
        yPos = screen.height() - 262
        xPos = screen.width() - 396
        self.move(xPos, yPos)
        # Lock on top
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)  # Important! Remove Border, Allow Transparency
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # Locks Maid
        self.setAttribute(Qt.WA_TranslucentBackground)  # Make window transparent (Needs Frameless Window)
        background = QPixmap("background.png")  # Get Image
        b_container = QLabel(self)  # Create Container for Background
        b_container.setPixmap(background)  # Set Container Image
        maid = QLabel(b_container)  # Create another container for the Maid

        # TEST /////////////////////////////
        # maid.setStyleSheet('border: 10px solid red;')  # Test
        b_container.setStyleSheet('border: 0px solid green;')


    # Right Click Menu
    def contextMenuEvent(self, event):
        maid_pic2 = QPixmap("jOn.png")
        menu = QMenu(self)
        quitAction = menu.addAction("Quit")
        closeAction = menu.addAction("Close this window")
        aboutAction = menu.addAction("About")
        next_maid = menu.addAction("Next")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == quitAction:
            sys.exit()  # self.close() for window close.
        elif action == closeAction:
            self.close()

    # Movement Handling
    def mouseMoveEvent(self, event):
        if (event.buttons() == Qt.LeftButton):
            self.move(event.globalPos().x() - self.drag_position.x(),
                      event.globalPos().y() - self.drag_position.y());
        event.accept()

    def mousePressEvent(self, event):
        if (event.button() == Qt.LeftButton):
            self.drag_position = event.globalPos() - self.pos();
        event.accept()


def init():
    app = QApplication(sys.argv)
    window = Window()
    animate = Animation()
    animate.start()
    window.show()
    app.exec_()


init()