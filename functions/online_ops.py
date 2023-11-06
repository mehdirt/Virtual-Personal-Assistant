import requests
import wikipedia
import pywhatkit as kit
from email.message import EmailMessage
import smtplib
from decouple import config

# Config enviroment variables
EMAIL = config('EMAIL')
PASSWORD = config('PASSWORD')
NEWS_API_KEY = config('NEWS_API_KEY')
WEATHER_API_KEY = config("WEATHER_API_KEY")
TMDB_API_KEY = config('TMDB_API_KEY')

def find_my_ip():
    ip_address = requests.get("https://api64.ipify.org/?format=json").json()
    return ip_address['ip']

def search_on_wikipedia(query):
    result = wikipedia.summary(query, sentences=2)
    return result

def play_on_youtube(video):
    kit.playonyt(video)

def search_on_google(query):
    kit.search(query)

def send_whatsapp_message(number, message):
    kit.sendwhatmsg_instantly(f"+98{number}", message)

def send_email(receiver_address, subject, message):
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

def get_latest_news():
    news_headlines = []
    res = requests.get(f"https://newsapi.org/v2/top-headlines?
                       country=us&apiKey={NEWS_API_KEY}&category=general").json()
    articles = res['articles']
    for article in articles:
        news_headlines.append(article['title'])
    return news_headlines[:5]

def get_weather_app(city): #TODO: test needed!
    res = requests.get(f"http://api.weatherapi.com/v1/current.json?
                      key={WEATHER_API_KEY}&q={city}").json()
    weather = res['condition:text']
    temperature = res['temp_c']
    feels_like = res['feelslike_c']
    return (weather, f"{temperature}℃", f"{feels_like}℃")

def get_trending_movies():
    trending_movies = []
    res = requests.get(
        f"https://api.themoviedb.org/3/trending/movie/day?api_key={TMDB_API_KEY}").json()
    results = res["results"]
    for r in results:
        trending_movies.append(r["original_title"])
    return trending_movies[:5]
