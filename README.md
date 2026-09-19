# AI Weather Assistant

A Flask web app that shows current conditions from OpenWeatherMap and optionally uses Groq for a concise weather tip. Without a Groq key, it uses a built-in practical tip.

## Setup

1. Create an OpenWeatherMap API key at https://openweathermap.org/api.
2. Add it to `.env` as `WEATHER_API_KEY=your_key`.
3. Optionally add a Groq key as `GROQ_API_KEY=your_key`.
4. Install and run:

```bash
python -m pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## API

`GET /api/weather?city=Mumbai` returns normalized current weather and advice as JSON.
