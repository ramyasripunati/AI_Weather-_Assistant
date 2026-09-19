"""Optional Groq-powered weather advice."""

import os
from typing import Any

from groq import Groq


def _fallback_advice(weather_data: dict[str, Any]) -> str:
    """Provide useful advice when no Groq key is configured or it is unavailable."""
    temperature, description = weather_data["temperature"], weather_data["description"].lower()
    if any(word in description for word in ("rain", "drizzle", "thunderstorm")):
        return "Take an umbrella and allow extra time for travel."
    if temperature >= 32:
        return "It is hot outside—drink water, seek shade, and use sunscreen."
    if temperature <= 10:
        return "It is chilly—wear a warm layer before heading out."
    if weather_data["wind_speed"] >= 30:
        return "It is quite windy, so secure loose items if you are going outdoors."
    return "Comfortable conditions overall; a light layer is a sensible choice."


def get_weather_advice(weather_data: dict[str, Any]) -> str:
    """Return brief practical advice, enhanced by Groq when configured."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return _fallback_advice(weather_data)
    prompt = ("Give one friendly, practical weather tip in at most 25 words. Do not use markdown. " f"Location: {weather_data['city']}, {weather_data['country']}. Conditions: {weather_data['description']}, " f"{weather_data['temperature']}°C, humidity {weather_data['humidity']}%, wind {weather_data['wind_speed']} km/h.")
    try:
        completion = Groq(api_key=api_key).chat.completions.create(model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant"), messages=[{"role": "user", "content": prompt}], temperature=0.4, max_tokens=60)
        advice = completion.choices[0].message.content
        if advice:
            return advice.strip()
    except Exception:
        pass
    return _fallback_advice(weather_data)
