import requests
import wikipedia
import pywhatkit as kit
from typing import List
from email.message import EmailMessage
import smtplib
from decouple import config

# Config enviroment variables
EMAIL = config('EMAIL')
PASSWORD = config('PASSWORD')
NEWS_API_KEY = config('NEWS_API_KEY')
OPENWEATHER_APP_ID = config("OPENWEATHER_APP_ID")
TMDB_API_KEY = config('TMDB_API_KEY')

def find_my_ip() -> str:
    """Finds the device's IP address"""
    ip_address = requests.get("https://api64.ipify.org/?format=json").json()
    return ip_address['ip']

def search_on_wikipedia(query) -> str:
    """Returns related result from Wikipedia"""
    result = wikipedia.summary(query, sentences=2)
    return result

def play_on_youtube(video) -> None:
    """Plays video on YouTube"""
    kit.playonyt(video)

def search_on_google(query) -> None:
    """Searches user's query on google"""
    kit.search(query)

def send_whatsapp_message(number: str, message: str) -> None:
    """Sends a WhatsApp message to a specific number"""
    kit.sendwhatmsg_instantly(f"+98{number}", message)

def send_email(receiver_address: str, subject: str, message: str) -> bool:
    """Sends a message to a specific email address"""
    try:
        email = EmailMessage()
        email['TO'] = receiver_address
        email['Subject'] = subject
        email['From'] = EMAIL
        email.set_content(message)
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login(EMAIL, PASSWORD)
        s.send_message(email)
        s.close()
        return True
    except Exception as e:
        print(e)
        return False

def get_latest_news() -> List[str]:
    """Retrieves the latest news headlines from a general category in the United States
    using the NewsAPI."""
    news_headlines = []
    res = requests.get(f"https://newsapi.org/v2/top-headlines?\
                       country=us&apiKey={NEWS_API_KEY}&category=general").json()
    articles = res['articles']
    for article in articles:
        news_headlines.append(article['title'])
    return news_headlines[:5]

def get_weather_report(city) -> List[str]: #TODO: test needed!
    """Fetches the current weather report for the specified city using the OpenWeatherMap API."""
    res = requests.get(f"http://api.openweathermap.org/data/2.5/weather?\
                       q={city}&appid={OPENWEATHER_APP_ID}&units=metric").json()
    weather = res["weather"][0]["main"]
    temperature = res["main"]["temp"]
    feels_like = res["main"]["feels_like"]
    return weather, f"{temperature}℃", f"{feels_like}℃"

def get_trending_movies() -> List[str]: # TODO: test nedded!
    trending_movies = []
    res = requests.get(
        f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}").json()
    results = res["results"]
    for r in results:
        trending_movies.append(r["original_title"])
    return trending_movies[:5]

def get_random_joke() -> str:
    header = {
        'Accept': 'application/json'
    }
    res = requests.get("https://icanhazdadjoke.com/", header=header).json()
    return res['joke']

def get_random_advice() -> str:
    res = requests.get("https://api.adviceslip.com/advice").json()
    return res['slip']['advice']
