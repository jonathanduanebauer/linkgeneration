# 🎙️ Today FM 80s – Link Generator with Weather, Traffic, and Promos

This Python script automatically generates short presenter-style talk links for **Today FM 80s**, blending weather, traffic updates, show promos, and fun facts between two 80s tracks.

Generated scripts are converted to audio using [ElevenLabs](https://www.elevenlabs.io/) text-to-speech API and saved as MP3s.

---

## 📂 What It Does

- Loads a CSV of 80s music tracks.
- Samples 5 songs to generate links between each pair.
- Adds:
  - Natural-sounding station promos
  - Current weather (OpenWeatherMap API)
  - Real-time traffic updates (TomTom API)
  - Fun facts (from the CSV or a fallback)
- Converts the text links to realistic voiceovers using ElevenLabs.
- Saves the resulting MP3s to a local output folder.

---

## 🧪 Example Script Output

> "You are listening to TodayFM 80s. That was 'Sweet Dreams' by Eurythmics. Don’t miss Dave Moore on Today FM — weekdays from 9 to midday, packed with laughs and great music. Right now in Dublin, it’s 17 degrees with light rain. This one was a massive tune back in the 80s — guaranteed to get you moving. Coming up next — 'Africa' by Toto."

---

## 📦 Requirements

Install dependencies via `pip`:

```bash
pip install pandas requests elevenlabs
