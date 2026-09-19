"""OpenWeatherMap current-weather API integration."""

import os
from typing import Any

import requests

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


class WeatherServiceError(Exception):
    """An expected, user-safe weather service error."""

    def __init__(self, message: str, status_code: int = 502) -> None:
        super().__init__(message)
        self.status_code = status_code


def get_weather(city: str) -> dict[str, Any]:
    """Fetch and normalize current metric weather data for ``city``."""
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        raise WeatherServiceError("Weather service is not configured. Add WEATHER_API_KEY to .env.", 503)
    try:
        response = requests.get(BASE_URL, params={"q": city, "appid": api_key, "units": "metric"}, timeout=10)
    except requests.RequestException as error:
        raise WeatherServiceError("Could not reach the weather service. Please try again.") from error
    if response.status_code == 404:
        raise WeatherServiceError("City not found. Check the spelling and try again.", 404)
    if response.status_code == 401:
        raise WeatherServiceError("The weather API key is invalid. Check WEATHER_API_KEY in .env.", 503)
    if not response.ok:
        raise WeatherServiceError("The weather service is temporarily unavailable. Please try again.")
    try:
        data = response.json()
        condition = data["weather"][0]
        return {"city": data["name"], "country": data["sys"]["country"], "temperature": round(data["main"]["temp"]), "feels_like": round(data["main"]["feels_like"]), "humidity": data["main"]["humidity"], "wind_speed": round(data["wind"]["speed"] * 3.6, 1), "description": condition["description"].capitalize(), "icon": condition["icon"]}
    except (KeyError, IndexError, TypeError, ValueError) as error:
        raise WeatherServiceError("The weather service returned incomplete data.") from error
