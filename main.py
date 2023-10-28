import pyttsx3
from decouple import config

USERNAME = config("USER")
BOTNAME = config("BOTNAME")

engine = pyttsx.init('sapi5')

# Set rate
engine.setProperty('rate', 190)

# Set volume
engine.setProperty('volume', 1.0)

# Set voice (female)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)