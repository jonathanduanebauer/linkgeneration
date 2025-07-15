import os
import datetime
import random
import requests
import pandas as pd
from elevenlabs.client import ElevenLabs

# Set ElevenLabs API key
client = ElevenLabs(api_key="sk_728a519a8615ae5817cc33cefd4bfc59fc40b6d5bafac70b")

# Voice ID for V2
VOICE_ID = "NiLLkhVjAqnvNUZHMpdJ"

# File paths
CSV_PATH = "/home/ftpuser/links/80s.csv"
OUTPUT_DIR = "/home/ftpuser/links/generated"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Weather and traffic API setup
WEATHER_API_KEY = "4d910c65923b7fb05958bf5727ad81d9"
TOMTOM_API_KEY = "rf4AQbwDITuFSKYePelocMnVmwN4lPyE"
CITIES = ["Dublin", "Cork", "Galway", "Donegal"]
TRAFFIC_CITIES = {"Dublin": (53.349805, -6.26031), "Galway": (53.2707, -9.0568)}

# Improved, more natural promo messages
PROMO_MESSAGES = [
    "Fancy winning some cash? Check out the latest winner and how to enter at cashmachine.ie.",
    "Love stations like this? You’ll find loads more on the GoLoud app — grab it from your app store.",
    "Ian Dempsey’s on Today FM from 6 to 9 every morning — the perfect way to start your day.",
    "Don’t miss Dave Moore on Today FM — weekdays from 9 to midday, packed with laughs and great music.",
    "Louise Cantillion brings good vibes on Today FM, every weekday from 12 to 2 — don’t miss it.",
    "Ray Foley is on from 2pm on Today FM — expect laughs, energy, and brilliant tunes.",
    "Catch up on the best of Today FM this week — head over to todayfm.com."
]

# Load and clean the CSV
df = pd.read_csv(CSV_PATH)
df.columns = df.columns.str.strip()
df = df[df['Artist'].notna() & df['Title'].notna()]
df = df[df['Artist'].str.strip() != ""].reset_index(drop=True)
sampled = df.sample(n=5).reset_index(drop=True)

# Helper: get weather
def get_weather(city):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},IE&units=metric&appid={WEATHER_API_KEY}"
        response = requests.get(url)
        data = response.json()
        temp = data['main']['temp']
        desc = data['weather'][0]['description']
        return f"Right now in {city}, it’s {int(temp)} degrees with {desc}."
    except:
        return "Weather’s looking pretty decent right around the country."

# Helper: get traffic
def get_traffic(city):
    if city not in TRAFFIC_CITIES:
        return ""
    lat, lon = TRAFFIC_CITIES[city]
    try:
        url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/relative0/10/json?point={lat}%2C{lon}&key={TOMTOM_API_KEY}"
        response = requests.get(url)
        data = response.json()
        current = data['flowSegmentData']['currentSpeed']
        freeflow = data['flowSegmentData']['freeFlowSpeed']
        if current < freeflow * 0.6:
            return f"Traffic in {city} is quite heavy right now."
        elif current < freeflow * 0.8:
            return f"Traffic in {city} is a little slow at the moment."
        else:
            return f"Traffic in {city} is moving well."
    except:
        return ""

# Helper: get fun fact
def get_fact(row):
    if 'Fact' in row and isinstance(row['Fact'], str) and row['Fact'].strip():
        return row['Fact']
    return "This one was a massive tune back in the 80s — guaranteed to get you moving."

# Generate links
for i in range(len(sampled) - 1):
    current = sampled.loc[i]
    next_up = sampled.loc[i + 1]

    promo = random.choice(PROMO_MESSAGES)
    city = random.choice(CITIES)
    weather = get_weather(city)
    fact = get_fact(next_up)
    traffic = get_traffic(random.choice(list(TRAFFIC_CITIES.keys()))) if random.random() < 0.4 else ""

    script = (
        f"You are listening to TodayFM 80s. "
        f"That was '{current['Title']}' by {current['Artist']}. "
        f"{promo} {weather} {traffic} {fact} "
        f"Coming up next — '{next_up['Title']}' by {next_up['Artist']}."
    )

    filename = f"link_{i}_{current['Title'].replace(' ', '_')}_to_{next_up['Title'].replace(' ', '_')}.mp3"
    filepath = os.path.join(OUTPUT_DIR, filename)

    print(f"🎤 Generating link {i}: {current['Title']} ➔ {next_up['Title']}")
    try:
        audio_stream = client.text_to_speech.convert(
            voice_id=VOICE_ID,
            model_id="eleven_multilingual_v2",
            text=script,
            output_format="mp3_44100_128"
        )
        with open(filepath, "wb") as f:
            for chunk in audio_stream:
                f.write(chunk)
        print(f"✅ Saved to {filepath}")
    except Exception as e:
        print(f"❌ Error on index {i}: {e}")
