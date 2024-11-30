import pyttsx3  # pip install pyttsx3
import datetime
import speech_recognition as sr  # pip install SpeechRecognition
import smtplib # inbuild library for emails sent
# from secrets import senderemail, epwd, to
import pyautogui
import webbrowser as web
from time import sleep
import wikipedia #pip install wikiedia
import pywhatkit
import requests
from newsapi import NewsApiClient #pip install newsapi-python & pip install newsapi
import clipboard
import os
import pyjokes
import time as tt

engine = pyttsx3.init()

# Define assistant_name as a global variable
assistant_name = "Jarvis"

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def getvoices(voice):
    global assistant_name  # Access the global variable
    voices = engine.getProperty('voices')
    if voice == 1:
        engine.setProperty('voice', voices[0].id)
        assistant_name = "Jarvis"
        speak("Hello, this is Jarvis.")
    elif voice == 2:
        engine.setProperty('voice', voices[1].id)
        assistant_name = "Friday"
        speak("Hello, this is Friday.")

def time():
    Time = datetime.datetime.now().strftime("%I:%M:%S")
    speak(f"The current time is {Time}")

def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    day = int(datetime.datetime.now().day)
    speak(f"The current date is {day}, {month}, {year}")

def greeting():
    hour = datetime.datetime.now().hour
    if 6 <= hour < 12:
        speak(f"Good morning!")
    elif 12 <= hour < 18:
        speak(f"Good afternoon!")
    elif 18 <= hour < 24:
        speak(f"Good evening!")
    else:
        speak(f"Good night!")

def wishme():
    speak("Assalamualaikum Boss! Welcome back!")
     # Uncomment below lines if you want the assistant to say the time and date
    # time()
    # date()
    greeting()
    speak(f"{assistant_name} at your service. Please tell me how I can help you!")

def takeCommandCMD():
    # """Take command from the user via the command line."""
    query = input("Please tell me how I can help you?\n")
    return query

# "pip install PyAudio" is required for speech recognition
def takeCommandMIC():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)  # Adjust for background noise
        r.pause_threshold = 1  # Pause before assuming the user is done speaking
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-IN")
        print(f"User said: {query}")
        return query
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        speak("Sorry, I did not understand that. Can you repeat?")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        speak("Network error. Please check your internet connection.")
        return None
    
# def sendEmail():
#     server = smtplib.SMTP('smtp.gmail.com', 587)
#     server.starttls()
#     server.login(senderemail, epwd)
#     server.sendmail(senderemail, to, 'hello this is test1 email by Jarvis')
#     server.close()
#     sendEmail()
#     email send option not coming due to gmail security policy updates.

def sendwhatsmsg(phone_no, message):
    Message =message
    web.open('https://web.whatsapp.com/send?phone='+phone_no+'&text='+Message)
    sleep(10)
    pyautogui.press('enter')

def searchgoogle():
    speak('what should I search for?')
    search = takeCommandMIC()
    web.open('https://www.google.com/search?q='+search)

def news():
    newsapi = NewsApiClient(api_key = '317768ba665b40d38f0d9c0a526fa956')
    data = newsapi.get_top_headlines(q = 'bitcoin',
                                        language='en',  
                                        page_size = 5)
    
    newsdata = data['articles']
    for x,y in enumerate(newsdata):
        print(f'{x}{y["description"]}')
        speak((f'{x}{y["description"]}'))

    speak("that's it for now i'll update you in some time")


def text2speech():
    text = clipboard. paste()
    print(text)
    speak(text)

def screenshot():
    name_img = tt.time()
    name_img = f'C:\\Users\\zubai\\OneDrive\\Desktop\\AI man\\Jarvis 2.0\\screenshot\\{name_img}.png'
    img = pyautogui.screenshot(name_img)
    img.show()

if __name__ == "__main__":
    # Choose a voice: 1 for male (Jarvis), 2 for female (Friday)
    getvoices(1)  # Change to 1 for Jarvis
    # wishme() enable for greetings
    while True:
        query = takeCommandMIC()
        
        # Check if query is None before processing
        if query is None:
            continue
        
        query = query.lower()

        if 'time' in query: # mention what is time
            time()
        elif 'date' in query: # what is date
            date()
        
        elif 'message' in query:
            user_name = {
                'Ahmed':'+91 93927 86721',
                'Taukir':'+91 72078 60754',
                'Farooq': '+91 79896 20990'
            }
            try:
                speak("To whom do you want to send the WhatsApp message?")
                name = takeCommandMIC()  # Assuming `takeCommandMIC` is a function to capture speech input
                phone_no = user_name[name]  # Assuming `user_name` is a dictionary with names as keys and phone numbers as values
                speak("What is the message?")
                message = takeCommandMIC()
                sendwhatsmsg(phone_no, message)  # Amention like "send message and then perrson name"
                speak("Message has been sent.")
            except Exception as e:
                print(e)
                speak("Unable to send the message.")
        
        elif 'wikipedia' in query:
            speak('searching on wikipedia...')
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences = 2)
            print(result)
            speak(result)

            #mention on wikipedia like this: " wikipedia about "topic".

        elif 'search' in query: #search on google
            searchgoogle()

        elif 'youtube' in query: # search on youtube, and then mention only topic "example: song name"
            speak("what should I search for on youtube?")
            topic = takeCommandMIC()
            pywhatkit.playonyt(topic)

        #https://api.openweathermap.org/data/2.5/weather?q=hyderabad&units=imperial&appid=d960fb0ab3e87a0b1266d3204211b64a
        elif 'weather' in query: # how is teh weather
            city = 'mumbai'
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid=d960fb0ab3e87a0b1266d3204211b64a'

            res = requests.get(url)
            data = res.json()

            weather = data['weather'][0]['main']
            temp = data['main']['temp']
            desp = data['weather'][0]['description']
            temp = round((temp - 32) * 5 / 9)

            print(weather)
            print(temp)
            print(desp)

            speak(f"The weather in {city} is like this:")
            speak(f"Temperature: {temp} degrees Celsius")
            speak(f"Weather is {desp}")

        elif 'news' in query:
            news()

        elif 'read' in query:
            text2speech()

        elif 'open code' in query: # open code
            codepath = 'C:\\Users\\zubai\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe'
            os.startfile(codepath)

        elif 'open' in query: #open my documents
            os.system('explorer C://{}'.format(query.replace('Open','')))

        elif 'joke' in query:
            speak(pyjokes.get_joke())

        elif 'screenshot' in query:
            screenshot()


        elif 'offline' in query: # mention " go offline  jarvis"
            quit()