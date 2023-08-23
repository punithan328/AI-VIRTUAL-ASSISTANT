import requests
from functions.online_ops import find_my_ip, get_latest_news, get_random_advice, get_random_joke, get_weather_report, play_on_youtube, search_on_google, search_on_wikipedia, send_email, send_whatsapp_message
import pyttsx3
import speech_recognition as sr
import sys
import os
from decouple import config
from datetime import datetime
from functions.os_ops import open_calculator, open_camera, open_cmd, open_notepad, open_discord
from random import choice
from utils import opening_text
from pprint import pprint
import webbrowser
import time
import qrcode
from state import state
import speedtest
import pywhatkit
import pywhatkit as kit
import pyjokes
import wikipedia
from pytube import YouTube
import PyPDF2
import smtplib
import psutil
import instaloader
from PhoneNumer import Phonenumber_location_tracker
import cv2
from Recordings import Record_Option

# . env/Scripts/activate

from pywikihow import search_wikihow
from bs4 import BeautifulSoup
import numpy as np 
import pyautogui
from PIL import ImageGrab
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer,QTime,QDate,Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from PyQt5.uic import loadUi
from JarvisUi import Ui_JarvisUI


USERNAME = config('USER')
BOTNAME = config('BOTNAME')
cpath = config('C_PATH')


engine = pyttsx3.init('sapi5')

# Set Rate
engine.setProperty('rate', 190)

# Set Volume
engine.setProperty('volume', 1.0)

# Set Voice (Female)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


# Text to Speech Conversion
def speak(text):
    """Used to speak whatever text is passed to it"""

    engine.say(text)
    engine.runAndWait()


# Greet the user
def greet_user():
    """Greets the user according to the time"""
    
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good Morning {USERNAME}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Good afternoon {USERNAME}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Good Evening {USERNAME}")
    speak(f"I am {BOTNAME}. How may I assist you?")


# Takes Input from User
def take_user_input():
    """Takes user input, recognizes it using Speech Recognition module and converts it into text"""
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening....')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        if not 'exit' in query or 'stop' in query:
            speak(choice(opening_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                speak("Good night sir, take care!")
            else:
                speak('Have a good day sir!')
            exit()
    except Exception:
        speak('Sorry, I could not understand. Could you please say that again?')
        query = 'None'
    return query
####

def wish():
    hour = int(datetime.now().hour)
    t = time.strftime("%I:%M %p")
    day = Cal_day()
    print(t)
    if (hour>=0) and (hour <=12) and ('AM' in t):
        speak(f'Good morning boss, its {day} and the time is {t}')
    elif (hour >= 12) and (hour <= 16) and ('PM' in t):
        speak(f"good afternoon boss, its {day} and the time is {t}")
    else:
        speak(f"good evening boss, its {day} and the time is {t}")

#Weather forecast
def temperature():
    IP_Address = requests.get('https://api.ipify.org').text
    url = 'https://get.geojs.io/v1/ip/geo/'+IP_Address+'.json'
    geo_reqeust = requests.get(url)
    geo_data = geo_reqeust.json()
    city = geo_data['city']
    search = f"temperature in {city}"
    url_1 = f"https://www.google.com/search?q={search}"
    r = requests.get(url_1)
    data = BeautifulSoup(r.text,"html.parser")
    temp = data.find("div",class_="BNeawe").text
    speak(f"current {search} is {temp}")
    print(f"current {search} is {temp}")

#qrCodeGenerator
def qrCodeGenerator():
    speak(f"Boss enter the text/link that you want to keep in the qr code")
    input_Text_link = input("Enter the Text/Link : ")
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=15,
        border=4,
    )
    QRfile_name = (str(datetime.now())).replace(" ","-")
    QRfile_name = QRfile_name.replace(":","-")
    QRfile_name = QRfile_name.replace(".","-")
    QRfile_name = QRfile_name+"-QR.png"
    qr.add_data(input_Text_link)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(f"QRCodes\{QRfile_name}")
    speak(f"Boss the qr code has been generated")

#Mobile camera
def Mobilecamra():
    import urllib.request
    import numpy as np
    try:
        speak(f"Boss openinging mobile camera")
        URL = "http://_IP_Webcam_IP_address_/shot.jpg" #Discription for this is available in the README file
        while True:
            imag_arr = np.array(bytearray(urllib.request.urlopen(URL).read()),dtype=np.uint8)
            img = cv2.imdecode(imag_arr,-1)
            cv2.imshow('IPWebcam',img)
            q = cv2.waitKey(1)
            if q == ord("q"):
                speak(f"Boss closing mobile camera")
                break
        cv2.destroyAllWindows()
    except Exception as e:
        print("Some error occured")

#Web camera
#NOTE to exit from the web camera press "ESC" key 
def webCam():    
    speak('Opening camera')
    cap = cv2.VideoCapture(0)
    while True:
        ret, img = cap.read()
        cv2.imshow('web camera',img)
        k = cv2.waitKey(50)
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()


#covid 
def Covid(s):
    try:
        from covid_india import states
        details = states.getdata()
        if "check in" in s:
            s = s.replace("check in","").strip()
            print(s)
        elif "check" in s:
            s = s.replace("check","").strip()
            print(s)
        elif "tech" in s:
            s = s.replace("tech","").strip()
        s = state[s]
        ss = details[s]
        Total = ss["Total"]
        Active = ss["Active"]
        Cured = ss["Cured"]
        Death = ss["Death"]
        print(f"Boss the total cases in {s} are {Total}, the number of active cases are {Active}, and {Cured} people cured, and {Death} people are death")
        speak(f"Boss the total cases in {s} are {Total}, the number of active cases are {Active}, and {Cured} people cured, and {Death} people are death")
        time.sleep(5)
        speak("Boss do you want any information of other states")
        I = take_user_input()
        print(I)
        if ("check" in I):
            Covid(I)
        elif("no" in I):
            speak("Okay boss stay home stay safe")
        else:
            speak("Okay boss stay home stay safe")
    except:
        speak("Boss some error occured, please try again")
        speak("Boss do you want any information of other states")
        I = take_user_input()
        if("yes" in I):
            speak("boss, Which state covid status do u want to check")
            Sta = take_user_input()
            Covid(Sta)
        elif("no" in I):
            speak("Okay boss stay home stay safe")
        else:
            speak("Okay boss stay home stay safe")

#Whatsapp
def whatsapp(query):
    try:
        query = query.replace('send a message to','')
        query = query.strip()
        name,numberID,F = SearchCont(query)
        if F:
            print(numberID)
            speak(f'Boss, what message do you want to send to {name}')
            message = take_user_input()
            hour = int(datetime.datetime.now().hour)
            min = int(datetime.datetime.now().minute)
            print(hour,min)
            if "group" in query:
                kit.sendwhatmsg_to_group(numberID,message,int(hour),int(min)+1)
            else:
                kit.sendwhatmsg(numberID,message,int(hour),int(min)+1)
            speak("Boss message have been sent")
        if F==False:
            speak(f'Boss, the name not found in our data base, shall I add the contact')
            AddOrNot = take_user_input()
            print(AddOrNot)
            if ("yes" in AddOrNot) or ("add" in AddOrNot) or ("yeah" in AddOrNot) or ("yah" in AddOrNot):
                AddContact()
            elif("no" in AddOrNot):
                speak('Ok Boss')
    except:
        print("Error occured, please try again")


#Add contacts
def AddContact():
    speak(f'Boss, Enter the contact details')
    name = input("Enter the name :").lower()
    number = input("Enter the number :")
    NumberFormat = f'"{name}":"+91{number}"'
    ContFile = open("Contacts.txt", "a") 
    ContFile.write(f"{NumberFormat}\n")
    ContFile.close()
    speak(f'Boss, Contact Saved Successfully')

#Search Contact
def SearchCont(name):
    with open("Contacts.txt","r") as ContactsFile:
        for line in ContactsFile:
            if name in line:
                print("Name Match Found")
                s = line.split("\"")
                return s[1],s[3],True
    return 0,0,False

#Display all contacts
def Display():
    ContactsFile = open("Contacts.txt","r")
    count=0
    for line in ContactsFile:
        count+=1
    ContactsFile.close()
    ContactsFile = open("Contacts.txt","r")
    speak(f"Boss displaying the {count} contacts stored in our data base")    
    for line in ContactsFile:
        s = line.split("\"")
        print("Name: "+s[1])
        print("Number: "+s[3])
    ContactsFile.close()

#search contact
def NameIntheContDataBase(query):
    line = query
    line = line.split("number in contacts")[0]
    if("tell me" in line):
        name = line.split("tell me")[1]
        name = name.strip()
    else:
        name= line.strip()
    name,number,bo = SearchCont(name)
    if bo:
        print(f"Contact Match Found in our data base with {name} and the mboile number is {number}")
        speak(f"Boss Contact Match Found in our data base with {name} and the mboile number is {number}")
    else:
        speak("Boss the name not found in our data base, shall I add the contact")
        AddOrNot = take_user_input()
        print(AddOrNot)
        if ("yes add it" in AddOrNot)or ("yeah" in AddOrNot) or ("yah" in AddOrNot):
            AddContact()
            speak(f'Boss, Contact Saved Successfully')
        elif("no" in AddOrNot) or ("don't add" in AddOrNot):
            speak('Ok Boss')

#Internet spped
def InternetSpeed():
    speak("Wait a few seconds boss, checking your internet speed")
    st = speedtest.Speedtest()
    dl = st.download()
    dl = dl/(1000000) #converting bytes to megabytes
    up = st.upload()
    up = up/(1000000)
    print(dl,up)
    speak(f"Boss, we have {dl} megabytes per second downloading speed and {up} megabytes per second uploading speed")
    
#Search for a process how to do
def How():
    speak("How to do mode is is activated")
    while True:
        speak("Please tell me what you want to know")
        how = take_user_input()
        try:
            if ("stop" in how) or("colose" in how):
                speak("Ok sir how to mode is closed")
                break
            else:
                max_result=1
                how_to = search_wikihow(how,max_result)
                assert len(how_to) == 1
                how_to[0].print()
                speak(how_to[0].summary)
        except Exception as e:
            speak("Sorry sir, I am not able to find this")

#Communication querys
def comum(query):
    print(query)
    if ('hi'in query) or('hai'in query) or ('hey'in query) or ('hello' in query) :
        speak("Hello boss what can I help for u")
    else :
        No_result_found()

#Fun querys to interact with jarvis
def Fun(query):
    print(query)
    if 'your name' in query:
        speak("My name is jarvis")
    elif 'my name' in query:
        speak("your name is Sujith")
    elif 'university name' in query:
        speak("you are studing in Amrita Vishwa Vidyapeetam, with batcheloe in Computer Science and Artificail Intelligence") 
    elif 'what can you do' in query:
        speak("I speak with you until you want to stop, I can say time, open your social media accounts,your open source accounts, open google browser,and I can also open your college websites, I can search for some thing in google and I can tell jokes")
    elif 'your age' in query:
        speak("I am very young that u")
    elif 'date' in query:
        speak('Sorry not intreseted, I am having headache, we will catch up some other time')
    elif 'are you single' in query:
        speak('No, I am in a relationship with wifi')
    elif 'joke' in query:
        speak(pyjokes.get_joke())
    elif 'are you there' in query:
        speak('Yes boss I am here')
    elif 'tell me something' in query:
        speak('boss, I don\'t have much to say, you only tell me someting i will give you the company')
    elif 'thank you' in query:
        speak('boss, I am here to help you..., your welcome')
    elif 'in your free time' in query:
        speak('boss, I will be listening to all your words')
    elif 'i love you' in query:
        speak('I love you too boss')
    elif 'can you hear me' in query:
        speak('Yes Boss, I can hear you')
    elif 'do you ever get tired' in query:
        speak('It would be impossible to tire of our conversation')
    else :
        No_result_found()

#Social media accounts querys
def social(query):
    print(query)
    if 'facebook' in query:
        speak('opening your facebook')
        webbrowser.open('https://www.facebook.com/')
    elif 'reddit' in query:
        speak('opening your whatsapp')
        webbrowser.open('https://web.whatsapp.com/')
    elif 'instagram' in query:
        speak('opening your instagram')
        webbrowser.open('https://www.instagram.com/')
    elif 'twitter' in query:
        speak('opening your twitter')
        webbrowser.open('https://twitter.com/Suj8_116')
    elif 'discord' in query:
        speak('opening your discord')
        webbrowser.open('https://discord.com/channels/@me')
    else :
        No_result_found()
    
#clock querys
def Clock_time(query):
    print(query)
    time = datetime.now().strftime('%I:%M %p')
    print(time)
    speak("Current time is "+time)

#calender day
def Cal_day():
    day = datetime.today().weekday() + 1
    Day_dict = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday',4: 'Thursday', 5: 'Friday', 6: 'Saturday',7: 'Sunday'}
    if day in Day_dict.keys():
        day_of_the_week = Day_dict[day]
        print(day_of_the_week)
    
    return day_of_the_week

#shedule function for remembering todays plans
#NOTE For example I have declared my college timetable you can declare anything you want
def shedule():
    day = Cal_day().lower()
    speak("Boss today's shedule is")
    Week = {"monday" : "Boss from 9:00 to 9:50 you have Cultural class, from 10:00 to 11:50 you have mechanics class, from 12:00 to 2:00 you have brake, and today you have sensors lab from 2:00",
    "tuesday" : "Boss from 9:00 to 9:50 you have English class, from 10:00 to 10:50 you have break,from 11:00 to 12:50 you have ELectrical class, from 1:00 to 2:00 you have brake, and today you have biology lab from 2:00",
    "wednesday" : "Boss today you have a full day of classes from 9:00 to 10:50 you have Data structures class, from 11:00 to 11:50 you have mechanics class, from 12:00 to 12:50 you have cultural class, from 1:00 to 2:00 you have brake, and today you have Data structures lab from 2:00",
    "thrusday" : "Boss today you have a full day of classes from 9:00 to 10:50 you have Maths class, from 11:00 to 12:50 you have sensors class, from 1:00 to 2:00 you have brake, and today you have english lab from 2:00",
    "friday" : "Boss today you have a full day of classes from 9:00 to 9:50 you have Biology class, from 10:00 to 10:50 you have data structures class, from 11:00 to 12:50 you have Elements of computing class, from 1:00 to 2:00 you have brake, and today you have Electronics lab from 2:00",
    "saturday" : "Boss today you have a full day of classes from 9:00 to 11:50 you have maths lab, from 12:00 to 12:50 you have english class, from 1:00 to 2:00 you have brake, and today you have elements of computing lab from 2:00",
    "sunday":"Boss today is holiday but we can't say anything when they will bomb with any assisgnments"}
    if day in Week.keys():
        speak(Week[day])

#college resources querys
#NOTE Below are some dummy links replace with your college website links
def college(query):
    print(query)
    if 'teams' in query:
        speak('opening your microsoft teams')
        webbrowser.open('https://teams.microsoft.com/')
    elif 'stream' in query:
        speak('opening your microsoft stream')
        webbrowser.open('https://web.microsoftstream.com/')
    elif 'outlook' in query:
        speak('opening your microsoft school outlook')
        webbrowser.open('https://outlook.office.com/mail/')
    elif 'amrita portal' in query:
        speak('opening your amrita university management system')
        webbrowser.open('https://aumsam.amrita.edu/')
    elif 'octave' in query:
        speak('opening Octave online')
        webbrowser.open('https://octave-online.net/')
    else :
        No_result_found()

#Online classes
def OnlineClasses(query):
    print(query)
    #Keep as many "elif" statemets based on your subject Eg: I have kept a dummy links for JAVA and mechanics classes link of MS Teams
    if("java" in query):
        speak('opening DSA class in teams')
        webbrowser.open("https://teams.microsoft.com/java")
    elif("mechanics" in query):
        speak('opening mechanics class in teams')
        webbrowser.open("https://teams.microsoft.com/mechanics")
    elif 'online classes' in query:
        speak('opening your microsoft teams')
        webbrowser.open('https://teams.microsoft.com/')

#Brower Search querys
def B_S(query):
    print(query)
    try:
        # ('what is meant by' in .query) or ('tell me about' in .query) or ('who the heck is' in .query)
        if ('wikipedia' in query):
            target1 = query.replace('search for','')
            target1 = target1.replace('in wikipedia','')
        elif('what is meant by' in query):
            target1 = query.replace("what is meant by"," ")
        elif('tell me about' in query):
            target1 = query.replace("tell me about"," ")
        elif('who the heck is' in query):
            target1 = query.replace("who the heck is"," ")
        print("searching....")
        info = wikipedia.summary(target1,5)
        print(info)
        speak("according to wikipedia "+info)
    except :
        No_result_found()
    
#Browser
def brows(query):
    print(query)
    if 'google' in query:
        speak("Boss, what should I search on google..")
        S = take_user_input()#taking query for what to search in google
        webbrowser.open(f"{S}")
    elif 'edge' in query:
        speak('opening your Chrome Browser')
        os.startfile('..\\..\\MicrosoftEdge.exe')#path for your edge browser application
    else :
        No_result_found()

#google applications selection
#if there is any wrong with the URL's replace them with your browsers URL's
def Google_Apps(query):
    print(query)
    if 'gmail' in query:
        speak('opening your google gmail')
        webbrowser.open('https://mail.google.com/mail/')
    elif 'maps' in query:
        speak('opening google maps')
        webbrowser.open('https://www.google.co.in/maps/')
    elif 'news' in query:
        speak('opening google news')
        webbrowser.open('https://news.google.com/')
    elif 'calender' in query:
        speak('opening google calender')
        webbrowser.open('https://calendar.google.com/calendar/')
    elif 'photos' in query:
        speak('opening your google photos')
        webbrowser.open('https://photos.google.com/')
    elif 'documents' in query:
        speak('opening your google documents')
        webbrowser.open('https://docs.google.com/document/')
    elif 'spreadsheet' in query:
        speak('opening your google spreadsheet')
        webbrowser.open('https://docs.google.com/spreadsheets/')
    else :
        No_result_found()
        
#youtube
def yt(query):
    print(query)
    if 'play' in query:
        speak("Boss can you please say the name of the song")
        song = take_user_input()
        if "play" in song:
            song = song.replace("play","")
        speak('playing '+song)
        print(f'playing {song}')
        kit.playonyt(song)
        print('playing')
    elif "download" in query:
        speak("Boss please enter the youtube video link which you want to download")
        link = input("Enter the YOUTUBE video link: ")
        yt=YouTube(link)
        yt.streams.get_highest_resolution().download()
        speak(f"Boss downloaded {yt.title} from the link you given into the main folder")
    elif 'youtube' in query:
        speak('opening your youtube')
        webbrowser.open('https://www.youtube.com/')
    else :
        No_result_found()
    
#Opensource accounts
def open_source(query):
    print(query)
    if 'github' in query:
        speak('opening your github')
        webbrowser.open('https://github.com/BolisettySujith')
    elif 'gitlab' in query:
        speak('opening your gitlab')
        webbrowser.open('https://gitlab.com/-/profile')
    else :
        No_result_found()

#Photo shops
def edit(query):
    print(query)
    if 'slides' in query:
        speak('opening your google slides')
        webbrowser.open('https://docs.google.com/presentation/')
    elif 'canva' in query:
        speak('opening your canva')
        webbrowser.open('https://www.canva.com/')
    else :
        No_result_found()

#OTT 
def OTT(query):
    print(query)
    if 'hotstar' in query:
        speak('opening your disney plus hotstar')
        webbrowser.open('https://www.hotstar.com/in')
    elif 'prime' in query:
        speak('opening your amazon prime videos')
        webbrowser.open('https://www.primevideo.com/')
    elif 'netflix' in query:
        speak('opening Netflix videos')
        webbrowser.open('https://www.netflix.com/')
    else :
        No_result_found()

#PC allications
#NOTE: place the correct path for the applications from your PC there may be some path errors so please check the applications places
#if you don't have any mentioned applications delete the codes for that
#I have placed applications path based on my PC path check while using which OS you are using and change according to it
def OpenApp(query):
    print(query)
    if ('calculator'in query) :
        speak('Opening calculator')
        os.startfile('C:\\Windows\\System32\\calc.exe')
    elif ('paint'in query) :
        speak('Opening msPaint')
        os.startfile('c:\\Windows\\System32\\mspaint.exe')
    elif ('notepad'in query) :
        speak('Opening notepad')
        os.startfile('c:\\Windows\\System32\\notepad.exe')
    elif ('discord'in query) :
        speak('Opening discord')
        os.startfile('..\\..\\Discord.exe')
    elif ('editor'in query) :
        speak('Opening your Visual studio code')
        os.startfile('..\\..\\Code.exe')
    elif ('online classes'in query) :
        speak('Opening your Microsoft teams')
        webbrowser.open('https://teams.microsoft.com/')
    elif ('spotify'in query) :
        speak('Opening spotify')
        os.startfile('..\\..\\Spotify.exe')
    elif ('lt spice'in query) :
        speak('Opening lt spice')
        os.startfile("..\\..\\XVIIx64.exe")
    elif ('steam'in query) :
        speak('Opening steam')
        os.startfile("..\\..\\steam.exe")
    elif ('media player'in query) :
        speak('Opening VLC media player')
        os.startfile("C:\Program Files\VideoLAN\VLC\vlc.exe")
    else :
        No_result_found()
        
#closeapplications function
def CloseApp(query):
    print(query)
    if ('calculator'in query) :
        speak("okay boss, closeing caliculator")
        os.system("taskkill /f /im calc.exe")
    elif ('paint'in query) :
        speak("okay boss, closeing mspaint")
        os.system("taskkill /f /im mspaint.exe")
    elif ('notepad'in query) :
        speak("okay boss, closeing notepad")
        os.system("taskkill /f /im notepad.exe")
    elif ('discord'in query) :
        speak("okay boss, closeing discord")
        os.system("taskkill /f /im Discord.exe")
    elif ('editor'in query) :
        speak("okay boss, closeing vs code")
        os.system("taskkill /f /im Code.exe")
    elif ('spotify'in query) :
        speak("okay boss, closeing spotify")
        os.system("taskkill /f /im Spotify.exe")
    elif ('lt spice'in query) :
        speak("okay boss, closeing lt spice")
        os.system("taskkill /f /im XVIIx64.exe")
    elif ('steam'in query) :
        speak("okay boss, closeing steam")
        os.system("taskkill /f /im steam.exe")
    elif ('media player'in query) :
        speak("okay boss, closeing media player")
        os.system("taskkill /f /im vlc.exe")
    else :
        No_result_found()

#Shopping links
def shopping(query):
    print(query)
    if 'flipkart' in query:
        speak('Opening flipkart online shopping website')
        webbrowser.open("https://www.flipkart.com/")
    elif 'amazon' in query:
        speak('Opening amazon online shopping website')
        webbrowser.open("https://www.amazon.in/")
    else :
        No_result_found()

#PDF reader
def pdf_reader():
    speak("Boss enter the name of the book which you want to read")
    n = input("Enter the book name: ")
    n = n.strip()+".pdf"
    book_n = open(n,'rb')
    pdfReader = PyPDF2.PdfFileReader(book_n)
    pages = pdfReader.numPages
    speak(f"Boss there are total of {pages} in this book")
    speak("plsase enter the page number Which I nedd to read")
    num = int(input("Enter the page number: "))
    page = pdfReader.getPage(num)
    text = page.extractText()
    print(text)
    speak(text)

#Time caliculating algorithm
def silenceTime(query):
    print(query)
    x=0
    #caliculating the given time to seconds from the speech commnd string
    if ('10' in query) or ('ten' in query):x=600
    elif '1' in query or ('one' in query):x=60
    elif '2' in query or ('two' in query):x=120
    elif '3' in query or ('three' in query):x=180
    elif '4' in query or ('four' in query):x=240
    elif '5' in query or ('five' in query):x=300
    elif '6' in query or ('six' in query):x=360
    elif '7' in query or ('seven' in query):x=420
    elif '8' in query or ('eight' in query):x=480
    elif '9' in query or ('nine' in query):x=540
    silence(x)
    
#Silence
def silence(k):
    t = k
    s = "Ok boss I will be silent for "+str(t/60)+" minutes"
    speak(s)
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
    speak("Boss "+str(k/60)+" minutes over")

#Mail verification
def verifyMail():
    try:
        speak("what should I say?")
        content = take_user_input()
        speak("To whom do u want to send the email?")
        to = take_user_input()
        SendEmail(to,content)
        speak("Email has been sent to "+str(to))
    except Exception as e:
        print(e)
        speak("Sorry sir I am not not able to send this email")

#Email Sender
def SendEmail(to,content):
    print(content)
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login("YOUR_MAIL_ID","PASWORD")
    server.sendmail("YOUR_MAIL_ID",to,content)
    server.close()

#location
def locaiton():
    speak("Wait boss, let me check")
    try:
        IP_Address = requests('https://api.ipify.org').text
        print(IP_Address)
        url = 'https://get.geojs.io/v1/ip/geo/'+IP_Address+'.json'
        print(url)
        geo_reqeust = requests(url)
        geo_data = geo_reqeust.json()
        city = geo_data['city']
        state = geo_data['region']
        country = geo_data['country']
        tZ = geo_data['timezone']
        longitude = geo_data['longitude']
        latidute = geo_data['latitude']
        org = geo_data['organization_name']
        print(city+" "+state+" "+country+" "+tZ+" "+longitude+" "+latidute+" "+org)
        speak(f"Boss i am not sure, but i think we are in {city} city of {state} state of {country} country")
        speak(f"and boss, we are in {tZ} timezone the latitude os our location is {latidute}, and the longitude of our location is {longitude}, and we are using {org}\'s network ")
    except Exception as e:
        speak("Sorry boss, due to network issue i am not able to find where we are.")
        pass

#Instagram profile
def Instagram_Pro():
    speak("Boss please enter the user name of Instagram: ")
    name = input("Enter username here: ")
    webbrowser.open(f"www.instagram.com/{name}")
    time.sleep(5)
    speak("Boss would you like to download the profile picture of this account.")
    cond = take_user_input()
    if('download' in cond):
        mod = instaloader.Instaloader()
        mod.download_profile(name,profile_pic_only=True)
        speak("I am done boss, profile picture is saved in your main folder. ")
    else:
        pass

#ScreenShot
def scshot():
    speak("Boss, please tell me the name for this screenshot file")
    name = take_user_input()
    speak("Please boss hold the screen for few seconds, I am taking screenshot")
    time.sleep(3)
    img = pyautogui.screenshot()
    img.save(f"{name}.png")
    speak("I am done boss, the screenshot is saved in main folder.")

#News
def news():
    MAIN_URL_= "https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=YOUR_NEWS_API_KEY"
    MAIN_PAGE_ = requests(MAIN_URL_).json()
    articles = MAIN_PAGE_["articles"]
    headings=[]
    seq = ['first','second','third','fourth','fifth','sixth','seventh','eighth','ninth','tenth'] #If you need more than ten you can extend it in the list
    for ar in articles:
        headings.append(ar['title'])
    for i in range(len(seq)):
        print(f"todays {seq[i]} news is: {headings[i]}")
        speak(f"todays {seq[i]} news is: {headings[i]}")
    speak("Boss I am done, I have read most of the latest news")

#System condition
def condition():
    usage = str(psutil.cpu_percent())
    speak("CPU is at"+usage+" percentage")
    battray = psutil.sensors_battery()
    percentage = battray.percent
    speak(f"Boss our system have {percentage} percentage Battery")
    if percentage >=75:
        speak(f"Boss we could have enough charging to continue our work")
    elif percentage >=40 and percentage <=75:
        speak(f"Boss we should connect out system to charging point to charge our battery")
    elif percentage >=15 and percentage <=30:
        speak(f"Boss we don't have enough power to work, please connect to charging")
    else:
        speak(f"Boss we have very low power, please connect to charging otherwise the system will shutdown very soon")
    
#no result found
def No_result_found():
    speak('Boss I couldn\'t understand, could you please say it again.')        



if __name__ == '__main__':
    greet_user()
    while True:
        query = take_user_input().lower()

        if 'open notepad' in query:
            open_notepad()

        elif 'open discord' in query:
            open_discord()

        elif 'open command prompt' in query or 'open cmd' in query:
            open_cmd()

        elif 'open camera' in query:
            open_camera()

        elif 'open calculator' in query:
            open_calculator()

        elif 'ip address' in query:
            ip_address = find_my_ip()
            speak(f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
            print(f'Your IP Address is {ip_address}')

        elif 'wikipedia' in query:
            speak('What do you want to search on Wikipedia, sir?')
            search_query = take_user_input().lower()
            results = search_on_wikipedia(search_query)
            speak(f"According to Wikipedia, {results}")
            speak("For your convenience, I am printing it on the screen sir.")
            print(results)

        elif 'youtube' in query:
            speak('What do you want to play on Youtube, sir?')
            video = take_user_input().lower()
            play_on_youtube(video)

        elif ('search on google' in query) or ('open google' in query) or ('google' in query):
            speak('What do you want to search on Google, sir?')
            query = take_user_input().lower()
            search_on_google(query)

        elif "send whatsapp message" in query:
            speak('On what number should I send the message sir? Please enter in the console: ')
            number = input("Enter the number: ")
            speak("What is the message sir?")
            message = take_user_input().lower()
            send_whatsapp_message(number, message)
            speak("I've sent the message sir.")

        elif "send an email" in query:
            speak("On what email address do I send sir? Please enter in the console: ")
            receiver_address = input("Enter email address: ")
            speak("What should be the subject sir?")
            subject = take_user_input().capitalize()
            speak("What is the message sir?")
            message = take_user_input().capitalize()
            if send_email(receiver_address, subject, message):
                speak("I've sent the email sir.")
            else:
                speak("Something went wrong while I was sending the mail. Please check the error logs sir.")

        elif 'joke' in query:
            speak(f"Hope you like this one sir")
            joke = get_random_joke()
            speak(joke)
            speak("For your convenience, I am printing it on the screen sir.")
            pprint(joke)

        elif "advice" in query:
            speak(f"Here's an advice for you, sir")
            advice = get_random_advice()
            speak(advice)
            speak("For your convenience, I am printing it on the screen sir.")
            pprint(advice)

        

        elif 'news' in query:
            speak(f"I'm reading out the latest news headlines, sir")
            speak(get_latest_news())
            speak("For your convenience, I am printing it on the screen sir.")
            print(*get_latest_news(), sep='\n')

        elif 'weather' in query:
            ip_address = find_my_ip()
            city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
            speak(f"Getting weather report for your city {city}")
            weather, temperature, feels_like = get_weather_report(city)
            speak(f"The current temperature is {temperature}, but it feels like {feels_like}")
            speak(f"Also, the weather report speaks about {weather}")
            speak("For your convenience, I am printing it on the screen sir.")
            print(f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")
        #####
        elif ("today" in query):
                day = Cal_day()
                speak("Today is "+day)

        elif ('play a song' in query) or ('open youtube' in query) or ("download a song" in  query) or ("download song" in  query) : 
        #querys for opening youtube, playing a song in youtube, and download a song in youtube
             yt( query) #function is from line 555
            #Interaction querys with JARVIS
        elif ('your age' in  query) or ('are you single'in  query) or ('are you there' in  query) or ('tell me something' in  query) or ('thank you' in  query) or ('in your free time' in  query) or ('i love you' in  query) or ('can you hear me' in  query) or ('do you ever get tired' in  query):
             Fun( query)
        elif 'time' in  query : 
             Clock_time( query)
        elif (('hi' in  query) and len( query)==2) or ((('hai' in  query) or ('hey' in  query)) and len( query)==3) or (('hello' in  query) and len( query)==5):
             comum( query)
        elif ('what can you do' in  query) or ('your name' in  query) or ('my name' in  query) or ('university name' in  query):
             Fun( query)
        elif ('joke'in  query) or ('date' in  query):
             Fun( query)
        #schedule querys for remembering you what is the planns of the day
        elif ("college time table" in  query) or ("schedule" in  query):
             shedule() #function is present from 407
        #It will tell the day Eg : Today is wednesday
        elif ("today" in  query):
            day =  Cal_day()
            speak("Today is "+day)
        #commad for opening any weekly meeting links
        #Eg: I have kept a meeting my amFOSS club 
        #Note: the given link is fake!!
        elif ("meeting" in  query):
             speak("Ok sir opening meeet")
             webbrowser.open("https://teams.microsoft.com/_#/pre-join-calling/19:meeting_NTE3OGFhMWUtZmU3Yy00NDVjLTlmMmQtNDZlNTRkMmYyMTFk@thread.v2")
        #query if you don't want the JARVIS to spack until for a certain time
        #Note: I can be silent for max of 10mins
        # Eg: JARVIS keep quiet for 5 minutes 
        elif ('silence' in  query) or ('silent' in  query) or ('keep quiet' in  query) or ('wait for' in  query) :
             silenceTime( query)
        #query for opening your social media accounts in webrowser
        #Eg : JARVIS open facebook (or) JARVIS open social media facebook 
        elif ('facebook' in  query) or ('whatsapp' in  query) or ('instagram' in  query) or ('twitter' in  query) or ('discord' in  query) or ('social media' in  query):
             social( query)
        #query for opening your OTT platform accounts
        #Eg: open hotstart
        elif ('hotstar' in  query) or ('prime' in  query) or ('netflix' in  query):
             OTT( query)
        #query for opening your online classes links
        elif ('online classes'in  query):
             OnlineClasses( query)
        #query for opeing college websites
        elif ('open teams'in  query) or ('open stream'in  query) or ('open sharepoint'in  query) or('open outlook'in  query)or('open amrita portal'in  query)or('open octave'in  query):
             college( query)
        #query to search for something in wikipedia
        #Eg: what is meant by python in wikipedia (or) search for "_something_" in wikipedia
        elif ('wikipedia' in  query) or ('what is meant by' in  query) or ('tell me about' in  query) or ('who the heck is' in  query):
             B_S( query)
        #query for opening your browsers and search for information in google
        
        #query to open your google applications
        elif ('open gmail'in  query) or('open maps'in  query) or('open calender'in  query) or('open documents'in  query )or('open spredsheet'in  query) or('open images'in  query) or('open drive'in  query) or('open news' in  query):
             Google_Apps( query)
        #query to open your open-source accounts
        #you can add other if you have
        elif ('open github'in  query) or ('open gitlab'in  query) :
             open_source( query)
        #querys to open presentaion makeing tools like CANVA and GOOGLE SLIDES
        elif ('slides'in  query) or ('canva'in  query) :
             edit( query)
        #query to open desktop applications
        #It can open : caliculator, notepad,paint, teams(aka online classes), discord, spotify, ltspice,vscode(aka editor), steam, VLC media player
        elif ('open calculator'in  query) or ('open notepad'in  query) or ('open paint'in  query) or ('open online classes'in  query) or ('open discord'in  query) or ('open ltspice'in  query) or ('open editor'in  query) or ('open spotify'in  query) or ('open steam'in  query) or ('open media player'in  query):
             OpenApp( query)
        #query to close desktop applications
        #It can close : caliculator, notepad,paint, discord, spotify, ltspice,vscode(aka editor), steam, VLC media player
        elif ('close calculator'in  query) or ('close notepad'in  query) or ('close paint'in  query) or ('close discord'in  query) or ('close ltspice'in  query) or ('close editor'in  query) or ('close spotify'in  query) or ('close steam'in  query) or ('close media player'in  query):
             CloseApp( query)
        #query for opening shopping websites 
        #NOTE: you can add as many websites
        elif ('flipkart'in  query) or ('amazon'in  query) :
             shopping( query)
        #query for asking your current location
        elif ('where i am' in  query) or ('where we are' in  query):
             locaiton()
        #query for opening query prompt 
        #Eg: jarvis open query prompt
        elif ('query prompt'in  query) :
             speak('Opening query prompt')
             os.system('start cmd')
        #query for opening an instagram profile and downloading the profile pictures of the profile
        #Eg: jarvis open a profile on instagram 
        elif ('instagram profile' in  query) or("profile on instagram" in  query):
             Instagram_Pro()
        #query for opening taking screenshot
        #Eg: jarvis take a screenshot
        elif ('take screenshot' in  query)or ('screenshot' in  query) or("take a screenshot" in  query):
             scshot()
        #query for reading PDF
        #EG: Jarvis read pdf
        elif ("read pdf" in  query) or ("pdf" in  query):
             pdf_reader()
        #query for searching for a procedure how to do something
        #Eg:jarvis activate mod
        #   jarvis How to make a cake (or) jarvis how to convert int to string in programming 
        elif ("activate mod" in  query) or ("activate mode" in query):
             How()
        #query for increaing the volume in the system
        #Eg: jarvis increase volume
        elif ("volume up" in  query) or ("increase volume" in  query):
             pyautogui.press("volumeup")
             speak('volume increased')
        #query for decreaseing the volume in the system
        #Eg: jarvis decrease volume
        elif ("volume down" in  query) or ("decrease volume" in  query):
             pyautogui.press("volumedown")
             speak('volume decreased')
        #query to mute the system sound
        #Eg: jarvis mute the sound
        elif ("volume mute" in  query) or ("mute the sound" in  query) :
             pyautogui.press("volumemute")
             speak('volume muted')
        #query for opening your mobile camera the description for using this is in the README file
        #Eg: Jarvis open mobile camera
        elif ("open mobile cam" in  query):
             Mobilecamra()
        #query for opening your webcamera
        #Eg: jarvis open webcamera
        elif ('web cam'in  query) :
             webCam()
        #query for creating a new contact
        elif("create a new contact" in  query):
             AddContact()
        #query for searching for a contact
        elif("number in contacts" in  query):
             NameIntheContDataBase( query)
        #query for displaying all contacts
        elif("display all the contacts" in  query):
             Display()
        #query for checking covid status in India
        #Eg: jarvis check covid (or) corona status
        elif ("covid" in  query) or  ("corona" in  query):
             speak("Boss which state covid 19 status do you want to check")
             s = take_user_input()
             Covid(s)
        #query for screenRecording
        #Eg: Jarvis start Screen recording
        elif ("recording" in  query) or ("screen recording" in  query) or ("voice recording" in  query):
            try:
                 speak("Boss press q key to stop recordings")
                 option =  query
                 Record_Option(option=option)
                 speak("Boss recording is being saved")
            except:
                 speak("Boss an unexpected error occured couldn't start screen recording")
        #query for phone number tracker
        elif ("track" in  query) or ("track a mobile number" in  query):
             speak("Boss please enter the mobile number with country code")
             try:
                 location,servise_prover,lat,lng=Phonenumber_location_tracker()
                 speak(f"Boss the mobile number is from {location} and the service provider for the mobile number is {servise_prover}")
                 speak(f"latitude of that mobile nuber is {lat} and longitude of that mobile number is {lng}")
                 print(location,servise_prover)
                 print(f"Latitude : {lat} and Longitude : {lng}")
                 speak("Boss location of the mobile number is saved in Maps")
             except:
                 speak("Boss an unexpected error occured couldn't track the mobile number")
        #query for playing a dowloaded mp3 song in which is present in your system
        #Eg: Jarvis play music
        elif 'music' in  query:
            try:
                music_dir = 'E:\\music' #change the song path directory if you have songs in other directory
                songs = os.listdir(music_dir)
                for song in songs:
                    if song.endswith('mp3'):
                        os.startfile(os.path.join(music_dir, song))
            except:
                 speak("Boss an unexpected error occured")
        #query for knowing your system IP address
        #Eg: jarvis check my ip address
        elif 'ip address' in  query:
            ip = requests('https://apiipifyorg').text
            print(f"your IP address is {ip}")
            speak(f"your IP address is {ip}")
        #query for seading a whatsapp group and individual message
        #Individual => Eg: send a message to sujith
        #group => Eg: send a message to school group NOTE: mention the name "group" otherwise jarvis cannot detect the name
        elif ('send a message' in  query):
             whatsapp( query)
        #query for sending an email 
        #Eg: jarvis send email
        elif 'dono' in  query:
             verifyMail()
        #query for checking the temperature in surroundings
        #jarvis check the surroundings temperature
        elif "temperature" in  query:
             temperature()
        #query to generate the qr codes
        elif ("create a qr code" in  query) or ("code generator" in query):
             qrCodeGenerator()
        #query for checking internet speed
        #Eg: jarvis check my internet speed
        elif "internet speed" in  query:
             InternetSpeed()
        #query to make the jarvis sleep
        #Eg: jarvis you can sleep now
        elif ("you can sleep" in  query) or ("sleep now" in  query):
             speak("Okay boss, I am going to sleep you can call me anytime")
             break
        #query for waking the jarvis from sleep
        #jarvis wake up
        elif ("wake up" in  query) or ("get up" in  query):
             speak("boss, I am not sleeping, I am in online, what can I do for u")
        #query for exiting jarvis from the program
        #Eg: jarvis goodbye
        elif ("goodbye" in  query) or ("get lost" in  query):
             speak("Thanks for using me boss, have a good day")
             sys.exit()
        #query for knowing about your system condition
        #Eg: jarvis what is the system condition
        elif ('system condition' in  query) or ('condition of the system' in  query):
             speak("checking the system condition")
             condition()
        #query for knowing the latest news
        #Eg: jarvis tell me the news
        elif ('tell me news' in  query) or ("the news" in  query) or ("todays news" in  query):
             speak("Please wait boss, featching the latest news")
             news()
        #query for shutting down the system
        #Eg: jarvis shutdown the system
        elif ('shutdown the system' in  query) or ('down the system' in  query):
             speak("Boss shutting down the system in 10 seconds")
             time.sleep(10)
             os.system("shutdown /s /t 5")
        #query for restarting the system
        #Eg: jarvis restart the system
        elif 'restart the system' in  query:
             speak("Boss restarting the system in 10 seconds")
             time.sleep(10)
             os.system("shutdown /r /t 5")
        #query for make the system sleep
        #Eg: jarvis sleep the system
        elif 'sleep the system' in  query:
              speak("Boss the system is going to sleep")
              os.system("rundll32.exe powrprof.dll, SetSuspendState 0,1,0")
    


class Main(QMainWindow):
    cpath ="C:/Users/Punithan/Desktop/JarvisFinal"
    
    def __init__(self,path):
        self.cpath = path
        super(QMainWindow, self).__init__()
        self.ui = Ui_JarvisUI(path=current_path)
        self.ui.setupUi(self)
        self.ui.pushButton_4.clicked.connect(self.startTask)
        self.ui.pushButton_3.clicked.connect(self.close)
        
    
    #NOTE make sure to place a correct path where you are keeping this gifs
    def startTask(self):
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}\UI\ironman1.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}\UI\ringJar.gif")
        self.ui.label_3.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}\UI\circle.gif")
        self.ui.label_4.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}\UI\lines1.gif")
        self.ui.label_7.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}\UI\ironman3.gif")
        self.ui.label_8.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}\UI\circle.gif")
        self.ui.label_9.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}\UI\powersource.gif")
        self.ui.label_12.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}\UI\powersource.gif")
        self.ui.label_13.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}\UI\ironman3_flipped.gif")
        self.ui.label_16.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie(rf"{self.cpath}\UI\Sujith.gif")
        self.ui.label_17.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(10)
        self.start()
        
    
    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)

current_path = os.getcwd()
app = QApplication(sys.argv)
jarvis = Main(path=current_path)
jarvis.show()
exit(app.exec_())


