'''
Name= Rishabh Kumar
email id: rinku87096@gmail.com
Speech To Text Module
VERSION = '2.0.0.1'

'''

import speech_recognition as sr 

def  AI_SpeechRecognition( 
    Pause_threshold=0.8,
    Timeout=2, 
    Phrase_time_limit=4,
    Snowboy_Configuration=None,
    Key=None, 
    language='en-US', 
    Show_all=False,
    ): ##AI_SpeechRecognition(1, 4, 7, 'en-in').lower()

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = Pause_threshold
        audio = r.listen(source,Timeout,Phrase_time_limit,Snowboy_Configuration)

    try:
        print("Recognizing..")
        query = r.recognize_google(audio, Key, language, Show_all)
        print(f"You Said : {query}")
    
    except:
        return "None"

    query = query
    return query

#AI_SpeechRecognition().lower()