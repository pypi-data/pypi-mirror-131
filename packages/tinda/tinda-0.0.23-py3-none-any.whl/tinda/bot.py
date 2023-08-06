
# dependencies:

from subprocess import list2cmdline
import speedtest
import socket
import requests
import threading
import pyttsx3 # text to speech
import random # random.randint(1, 10)
import os
import pynput # keyboard and mouse utility
import time
from datetime import datetime
from datetime import date
import pyautogui # mouse and keyboard utility
import speech_recognition  # pip install SpeechRecognition (working currently py -3.9)
import webbrowser # webbrowser.open("https://www.google.com")
import wikipedia # pip install wikipedia



class XXX:
    def __init__(self):
        self.days = {'0':'Monday',
        '1':'Tuesday',
        '2':'Wednesday',
        '3':'Thursday',
        '4':'Friday',
        '5':'Saturday',
        '6':'Sunday'}
        self.months = {'1':'Janauary',
            '2':'February',
            '3':'March',
            '4':'April',
            '5':'May',
            '6':'June',
            '7':'July',
            '8':'August',
            '9':'September',
            '10':'October',
            '11':'November',
            '12':'December'}
        # self.info
        self.name = "An A.I. has no name"
        self.age = "binary"
        self.bias = "not 'utf-8'"
        self.saying = "hor das aamb bhaldi?"
        # self.skills
        # text to speech
        self.task = pyttsx3.init()
        self.rate = self.task.getProperty('rate')
        self.task.setProperty('rate', 150)
        self.volume = self.task.getProperty('volume')
        self.task.setProperty('volume', 1)
        voices = self.task.getProperty('voices')
        self.task.setProperty('voice', voices[1].id)
        # webbrowser
        self.b = webbrowser
    def say(self, audio):
        self.task.say(audio)
        self.task.runAndWait()
    def randomNumber(self):
        return random.randint(0000, 9999)
    def execute(self, path):
        os.startfile(path)
    def repeatAfterMe(self):
        self.task.say(input("Enter what to say: "))
        self.task.runAndWait()
    def type(self, text):
        x = pynput.keyboard.Controller()
        time.sleep(3)
        x.type(text)
    def mousePosition(self):
        x = pynput.mouse.Controller()
        return x.position
    def goToPosition(self, x=0, y=0):
        x = pynput.mouse.Controller()
        x.position = (x, y)
    def leftClick(self):
        x = pynput.mouse.Controller()
        y = pynput.mouse.Button
        x.press(y.left)
        x.release(y.left)
    def rightClick(self):
        x = pynput.mouse.Controller()
        y = pynput.mouse.Button
        x.press(y.right)
        x.release(y.right)
    def time(self):
        x = datetime.now()
        x24 = x.strftime('%H:%M')
        x12 = x.strftime('%I:%M %p')
        time = str(x12)
        return time
    def date(self):
        today = date.today()
        weekday = str(today.weekday())
        day = str(today.day)
        month = str(today.month)
        year = str(today.year)
        #x= (f"Today is: {self.days[weekday]}, {day} {self.months[month]}, {year}.")
        x = {'weekday': self.days[weekday], 'date': day, 'month': self.months[month], 'year': year}
        return x
    def greet(self):
        x = datetime.now().hour
        if x >=0 and x < 12:
            return "Good Morning"
        elif x >=12 and x < 18:
            return "Good Afternoon"
        else:
            return "Good Evening"
    def showDesktop(self):
        try:
            pyautogui.hotkey('winleft', 'd')
        except:
            try:
                pyautogui.keyDown('winleft')
                pyautogui.press('d')
                pyautogui.keyUp('winleft')
            except:
                pass
    def listen(self):
        x = speech_recognition.Recognizer()
        with speech_recognition.Microphone() as source:
            x.adjust_for_ambient_noise(source)
            y = x.listen(source)
            try:
                r = x.recognize_google(y)
                print(f"#ZOE: #I heard: '{r}'")
            except speech_recognition.UnknownValueError:
                x = speech_recognition.Recognizer()
                r = XXX.listen(self)
            except speech_recognition.RequestError as e:
                r = XXX.listen(self)
        return r
    @staticmethod
    def listenOnce():
        r = speech_recognition.Recognizer()
        with speech_recognition.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            x = r.listen(source)
            data = r.recognize_google(x)
            return data
    def pyaudioWindowInstall(self):
        os.system("pip install pipwin")
        os.system("pipwin install pyaudio")
        os.system("python -m pip install pyaudio")
    def playMusic(self, path):
        x = os.listdir(path)
        os.startfile(os.path.join(path, random.choice(x)))
    def showdown(self):
        try:
            os.system("shutdown /s /t 1")
        except:
            return "Negavite"
    def cancelShutdown(self):
        try:
            os.system("shutdown /a")
        except:
            return "Negavite"
    def open(self, url): # webbrowser open
        self.b.open(url)
    def wiki(self, text): # wikipedia search
        return wikipedia.search(text)
    def wikiSummary(self, text): # wikipedia summary
        wikipedia.set_lang("en")
        return wikipedia.summary(text, sentences=2)
    def image(self, text): # google image search
        self.b.open(f'https://www.google.com/search?q={text}&tbm=isch')
    def google(self, text): # google search
        self.b.open(f'https://www.google.com/search?q={text}')
    def youtube(self, text): # youtube search
        self.b.open(f'https://www.youtube.com/results?search_query={text}')
    def stackoverflow(self, text): # stackoverflow search
        self.b.open(f'https://stackoverflow.com/search?q={text}')
    def github(self, text): # github search
        self.b.open(f'https://github.com/search?q={text}')
    @staticmethod
    def getIp(): # get ip address
        localIP = socket.gethostbyname(socket.gethostname())
        publicIP = requests.get('http://ip.42.pl/raw').text
        return f"Local IP: '{localIP}', Public IP: '{publicIP}'"
    @staticmethod
    def getLocation(): # get location
        x = requests.get('http://ip-api.com/json/')
        x = x.json()
        return f"City: '{x['city']}', Region: '{x['regionName']}', Country: '{x['country']}, Timezone: '{x['timezone']}', Service Provider: '{x['isp']}'"
    @staticmethod
    def speedtest(): # internet speed test
        x = speedtest.Speedtest()
        x.get_best_server()
        t = x.get_best_server()
        info = f" Server located in: {t['country']}, {t['sponsor']}, {t['name']}"
        print(info)
        down = x.download()
        up = x.upload()
        ping = x.results.ping
        r = f"Download: '{down/1024/1024 : .2f}' Mbps, Upload: '{up/1024/1024 : .2f}' Mbps, Ping: '{ping}' ms"
        return r


class ZOE:
    def __init__(self):
        self.name = "ZOE"
        self.age = "BINARY"
        self.bias = "not 'utf-8'"
        self.i = XXX()
    def creep(self):
        for i in range(3):
            print('\n')
        print("ZOE: Initiating creep protocol.")
        self.i.say("Initiating creep protocol.")
        for i in range(2):
            print('\n')
        print(self.i.greet())
        self.i.say(self.i.greet())
        print(self.i.date())
        print(f'The time is: {self.i.time()}')
        self.i.say(f'The time is: {self.i.time()}')
        for i in range(3):
            print('\n')
        print("ZOE: On Standby, waiting for further instructions.")
        self.i.say("On Standby, waiting for further instructions.")
        while True:
            x = self.i.listen().lower()
            if x == 0:
                continue
            if "zoe" in x:
                print(f"That is one of my aliases, {x}")
            if "what time" in x:
                print(f'The time is: {self.i.time()}')
                self.i.say(f'The time is: {self.i.time()}')
            if "stop" in x:
                print("ZOE: Terminating creep protocol.")
                self.i.say("Bye.")
                break
            if "what date" in x:
                print(f'The date is: {self.i.date()}')
                self.i.say(f'{self.i.date()}')
            if "get mouse position" in x:
                print(self.i.mousePosition())
                self.i.say("Roger that!")
            if "left-click" in x:
                self.i.leftClick()
                self.i.say("Roger that!")
            if "right-click" in x:
                self.i.rightClick()
                self.i.say("pew pew!")
            if "show desktop" in x:
                self.i.showDesktop()
                self.i.say("jooosh!")
            if "open browser" in x:
                self.i.open("www.google.com")
                self.i.say("right up!")
            if "image search" in x:
                self.i.say("What do you want to search for?")
                query = self.i.listenOnce()
                self.i.image(query)
                self.i.say("Roger that!")
            if "google search" in x:
                self.i.say("What are we looking for?")
                query = self.i.listenOnce()
                self.i.google(query)
            if "youtube search" in x:
                self.i.say("What are we looking for?")
                query = self.i.listenOnce()
                self.i.youtube(query)
            if "stackoverflow search" in x:
                self.i.say("What are we looking for?")
                query = self.i.listenOnce()
                self.i.stackoverflow(query)
            if "github search" in x:
                self.i.say("What are we looking for?")
                query = self.i.listenOnce()
                self.i.github(query)
            if "what ip" in x:
                print(self.i.getIp())
                self.i.say(self.i.getIp())
            if "what location" in x:
                print(self.i.getLocation())
                self.i.say(self.i.getLocation())
            if "internet speed test" in x:
                print("ZOE: Please wait, this could take a moment.")
                self.i.say("please wait, this could take a moment.")
                self.i.speedtest()







