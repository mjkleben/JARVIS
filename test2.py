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


def googler(to_search_for):  # opens a google page in a new window
    try:
        print("Searching on Google...")

        search = to_search_for
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
        print("------------------------------------------------------")
        result = soup.findAll("div", "")
        print((result))
        for i in result:
            print(i + "\n")
    except Exception as e:
        print(e)
googler("https://www.youtube.com/watch?v=OwJPPaEyqhI")
