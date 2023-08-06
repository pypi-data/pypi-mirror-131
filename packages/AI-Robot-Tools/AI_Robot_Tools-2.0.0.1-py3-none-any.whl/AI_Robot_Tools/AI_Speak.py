'''
Name= Rishabh Kumar
email id: rinku87096@gmail.com
Speak Module
VERSION = '2.0.0.1'

'''

import pyttsx3
from gtts import gTTS

def Speak(
    value,
    speed,
    Text: str
    ): #####Speak(0,150,'Hai I am Rishabh Kumar')
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    # print(voices[0].id)
    engine.setProperty('voices', voices[value].id)
    engine.setProperty('rate', speed)
    engine.say(Text)
    #print(Text)
    engine.runAndWait()

def Auto_Speak(Text: str): #####Speak('Hai I am Rishabh Kumar')
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    # print(voices[0].id)
    engine.setProperty('voices', voices[0].id)
    engine.setProperty('rate', 150)
    engine.say(Text)
    engine.runAndWait()

def TTOS(text,filename):
    try:
        tts = gTTS(text=text)
        file1 = str(filename+".mp3")
        tts.save(file1)
    except:
        None    

#Speak(0,150,'Hai How Are You I am Rishabh .')
#AI_Speak('Hai How Are You .')
TTOS("i am boy","iam")