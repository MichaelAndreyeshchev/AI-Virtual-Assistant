import os
import time
import wolframalpha
import json
import requests
import pyttsx3
import datetime
import wikipedia
import webbrowser
import subprocess
import speech_recognition as sr
from ecapture import ecapture as ec


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', 'voices[0].id')

def speak(text):
    engine.say(text)
    engine.runAndWait()

def greet():
    hour = datetime.datetime.now().hour

    if hour >= 0 and hour < 12:
        speak("Hello, Good Morning")
        print("Hello, Good Morning")

    elif hour >= 12 and hour < 18:
        speak("Hello, Good Afternoon")
        print("Hello, Good Afternoon")

    else:
        speak("Hello, Good Evening")
        print("Hello, Good Evening")

def command():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

        try:
            statement = r.recognize_google(audio, language = 'en')
            print(f"user said: {statement}\n")

        except Exception as e:
            speak("I am sorry. I do not understand what you said. Please repeat that again.")
            return "None"

        return statement
    
print("Loading...")
speak("Loading system")
greet()

if __name__=='__main__':
    while True:
        speak("How can I help you?")
        statement = command().lower()

        if statement == 0:
            continue

        if "good bye" in statement or "ok bye" in statement or "stop" in statement:
            speak('Good bye')
            print('Good bye')
            break

        if 'wikipedia' in statement:
            speak('Searching Wikipedia...')
            statement = statement.replace("wikipedia", "")
            results = wikipedia.summary(statement, sentences = 3)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in statement:
            webbrowser.open_new_tab("https://www.youtube.com")
            speak("youtube is now open")
            time.sleep(5)

        elif 'open google' in statement:
            webbrowser.open_new_tab("https://www.google.com")
            speak("Google is now open")
            time.sleep(5)

        elif 'open gmail' in statement:
            webbrowser.open_new_tab("gmail.com")
            speak("Google Mail is now open")
            time.sleep(5)

        elif 'time' in statement:
            timeStr = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"the time is {timeStr}")

        elif 'news' in statement:
            news = webbrowser.open_new_tab("https://news.google.com/topstories?hl=en-US&gl=US&ceid=US:en")
            speak("Here are some headlines from Google News")
            time.sleep(6)

        elif 'camera' in statement or 'take a photo' in statement:
            time_str = datetime.datetime.now().strftime('%m/%d/%Y')
            ec.capture(str(0), "Camera", time_str + ".jpg")

        elif 'search' in statement:
            statement = statement.replace("search", "")
            webbrowser.open_new_tab(statement)
            time.sleep(5)

        elif 'ask' in statement:
            speak('What geographical or computational questions would you like me to answer?')
            question = command()
            app_id = "ENTER HERE!!!"
            client = wolframalpha.Client(app_id) # app ID generated when you log on to wolfram alpha and in the My Apps (API) section you select Get APP_ID
            res = client.query(question)
            answer = next(res.results).text
            speak(answer)
            print(answer)

        elif 'who are you' in statement or 'what can you do' in statement:
            speak('I am an artificial intelligence system that is designed to open youtube, google chrome, gmail and stackoverflow, predict time, take photos, search wikipedia, predict the weather, get top headline news from Google News and answer computational or geographical questions')


        elif 'who made you' in statement or 'who created you' in statement or 'who discovered you' in statement:
            speak("I was created by Michael")
            print("I was created by Michael")

        elif 'weather' in statement:
            api_key = "ENTER HERE!!!"
            base_url = "https://api.openweathermap.org/data/2.5/weather?"
            speak("what is the city name")
            city_name = command()
            complete_url = base_url+"appid="+api_key+"&q="+city_name
            response = requests.get(complete_url)
            x = response.json()

            if x["cod"] != "404":
                y = x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(" Temperature in kelvin is " +
                      str(current_temperature) +
                      "\n humidity percentage is " +
                      str(current_humidiy) +
                      "\n description  " +
                      str(weather_description))
                print(" Temperature in kelvin = " +
                      str(current_temperature) +
                      "\n humidity (percentage) = " +
                      str(current_humidiy) +
                      "\n description = " +
                      str(weather_description))
        
        elif 'log off' in statement or 'sign out' in statement:
            speak("Computer is shutting down!")
            subprocess.call(["shutdown", "/l"])
			
time.sleep(3)