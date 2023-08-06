'''
Name= Rishabh Kumar
email id: rinku87096@gmail.com
AI Tools Module
VERSION = '2.0.0.1'

'''

from googletrans import Translator
import datetime
import time

def AI_Translate(
    Text: str,
    language='en', 
    Src='auto'
    ):## AI_Translate('Hai I am Rishabh','hi')
    translate = Translator()
    result = translate.translate(Text,dest=language,src=Src)
    Text_res = result
    return Text_res

#aa=AI_Translate('I am Rishabh',language='hi')
#print(aa.text)

Current_Time=time.strftime("%I:%M %p")
Current_Date=today = datetime.date.today()

NonePass=""
   
def AI_Wish_Time_Date(
    morning=Current_Time,
    afternoon=Current_Time,
    evening=Current_Time,
    night=Current_Time,
    Time_Show=NonePass,
    Date_Show=NonePass,
    otherText=NonePass
    ):## AI_Wish_Time_Date(morning=f"{Current_Date} {Current_Time}",afternoon=f"Afternoon The Time Is {Current_Time}",otherText="My Name is Rishabh")
    hour = int(datetime.datetime.now().hour)

    if 4 <= hour <=11:
        return (f"{morning} {Time_Show} {otherText} {Date_Show}")
    elif 12 <= hour <= 17:
        return (f"{afternoon} {Time_Show} {otherText} {Date_Show}")
    elif 18 <= hour <= 22:
        return (f"{evening} {Time_Show} {otherText} {Date_Show}")       
    else:
        return (f"{night} {Time_Show} {otherText} {Date_Show}")

#aa=AI_Wish_Time_Date(morning=f"{Current_Date} {Current_Time}",afternoon=f"Afternoon The Time Is {Current_Time}",otherText="My Name is Rishabh")
#print(aa)

