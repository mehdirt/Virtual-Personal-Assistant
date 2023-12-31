import pyttsx3
import speech_recognition as sr
from decouple import config
from datetime import datetime
from random import choice
from utils import opening_text
import requests
from pprint import pprint
from functions import open_camera, open_notepad, open_cmd, open_calculator, open_discord, \
find_my_ip, search_on_google, search_on_wikipedia, send_email, \
send_whatsapp_message, get_latest_news, get_random_advice, get_random_joke, get_trending_movies, get_weather_report, play_on_youtube

# Config enviroment variables
USERNAME = config("USER")
BOTNAME = config("BOTNAME")

engine = pyttsx3.init("sapi5")

# Set rate
engine.setProperty('rate', 170)

# Set volume
engine.setProperty('volume', 1.0)

# Set voice (female)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Text to speech conversion
def speak(txt: str) -> None:
    """Used to speak whatever text is passed to it."""
    engine.say(txt)
    engine.runAndWait()

# Greeting function
def greet_user() -> None:
    """Greets the user according to the time"""
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good Morning {USERNAME}")
    elif (hour >= 12) and (hour < 16):
        speak(f"Good afternoon {USERNAME}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Good Evening {USERNAME}")
    speak(f"I am {BOTNAME}. How may I assist you?")

# Take input from user
def take_user_input() -> str:
    """Takes user input, recognizes it using Speech Recognition module and converts it into text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print('Recognizing...')
        query = r.recognize_google(audio)
        if not 'exit' in query or 'stop' in query or 'bye' in query:
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

        elif 'search on google' in query:
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

        elif "trending movies" in query:
            trending_movies = get_trending_movies()
            speak(f"Some of the trending movies are: {trending_movies}")
            speak("For your convenience, I am printing it on the screen sir.")
            print(*trending_movies, sep='\n')

        elif 'news' in query:
            latest_news = get_latest_news()
            speak(f"I'm reading out the latest news headlines, sir")
            speak(latest_news)
            speak("For your convenience, I am printing it on the screen sir.")
            print(*latest_news, sep='\n')

        elif 'weather' in query:
            ip_address = find_my_ip()
            city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
            speak(f"Getting weather report for your city {city}")
            weather, temperature, feels_like = get_weather_report(city)
            speak(f"The current temperature is {temperature}, but it feels like {feels_like}")
            speak(f"Also, the weather report talks about {weather}")
            speak("For your convenience, I am printing it on the screen sir.")
            print(f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")