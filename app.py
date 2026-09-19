import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from services.groq_service import get_weather_advice
from services.weather_service import WeatherServiceError, get_weather

load_dotenv()
app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


@app.route("/")
def index():
    return render_template("index.html")


@app.get("/api/weather")
def weather():
    """Return current weather and concise AI advice for a requested city."""
    city = request.args.get("city", "").strip()
    if not city:
        return jsonify(error="Enter a city name first."), 400
    if len(city) > 100:
        return jsonify(error="City name must be 100 characters or fewer."), 400
    try:
        weather_data = get_weather(city)
        weather_data["advice"] = get_weather_advice(weather_data)
        return jsonify(weather_data)
    except WeatherServiceError as error:
        return jsonify(error=str(error)), error.status_code
    except Exception:
        app.logger.exception("Unexpected error while processing weather request")
        return jsonify(error="Something went wrong. Please try again."), 500


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
