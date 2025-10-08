import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import requests
import json
import google.generativeai as genai
import datetime as dt

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
CORS(app)

start_time = dt.datetime.now()

def _heuristic_advice(temperature, description):
    desc = (description or "").lower()
    temp = temperature if isinstance(temperature, (int, float)) else None

    # Dressing
    if temp is None:
        dressing = "Comfortable layers; adjust based on wind and precipitation."
    elif temp <= 5:
        dressing = "Heavy coat, thermal layers, gloves, and a warm hat."
    elif temp <= 15:
        dressing = "Light coat or sweater; consider a scarf."
    elif temp <= 25:
        dressing = "T-shirt or light long-sleeve; breathable fabrics."
    else:
        dressing = "Light, breathable clothing; hat and sunglasses."

    if "rain" in desc or "drizzle" in desc:
        dressing += " Carry a waterproof jacket or umbrella."
    if "snow" in desc:
        dressing += " Waterproof boots with good traction."
    if "wind" in desc:
        dressing += " Windbreaker recommended."

    # Drinks
    if temp is None or temp >= 22:
        drinks = "Plenty of water; consider electrolyte drinks if outdoors."
    elif temp >= 10:
        drinks = "Water or warm tea; stay hydrated."
    else:
        drinks = "Warm beverages like tea, cocoa, or soup."

    # Cautions
    cautions = []
    if temp is not None and temp >= 30:
        cautions.append("Avoid midday sun; apply SPF 30+; frequent shade breaks.")
    if temp is not None and temp <= 0:
        cautions.append("Watch for ice; limit exposure to prevent frostbite.")
    if "rain" in desc or "drizzle" in desc:
        cautions.append("Slippery surfaces; allow extra travel time.")
    if "snow" in desc:
        cautions.append("Reduced visibility and traction; drive carefully.")
    if "wind" in desc:
        cautions.append("Secure loose items; be cautious near trees and signage.")
    if "thunderstorm" in desc or "storm" in desc:
        cautions.append("Seek shelter; avoid open fields and tall isolated objects.")

    return {
        "dressing": dressing,
        "drinks": drinks,
        "cautions": cautions or ["Stay aware of changing conditions and local advisories."]
    }


def _ai_advice(temperature, description, city):
    api_key = os.getenv("GOOGLE_AI_API_KEY")
    if not api_key:
        return None
    try:
        genai.configure(api_key=api_key)
        model_name = os.getenv("GOOGLE_AI_MODEL", "gemini-1.5-flash")
        model = genai.GenerativeModel(model_name)

        prompt = (
            "You are a concise weather lifestyle assistant. Based on the inputs, "
            "return a STRICT JSON object with keys: dressing (string), drinks (string), cautions (array of strings).\n"
            f"City: {city}\n"
            f"Temperature (Celsius): {temperature}\n"
            f"Conditions: {description}\n"
            "Only return JSON, no extra text."
        )
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Ensure we parse a JSON object
        advice = json.loads(text)
        # Basic shape validation
        if not isinstance(advice, dict):
            return None
        if "dressing" not in advice or "drinks" not in advice or "cautions" not in advice:
            return None
        if not isinstance(advice.get("cautions"), list):
            advice["cautions"] = [str(advice.get("cautions"))]
        return advice
    except Exception:
        return None


@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city", default="", type=str).strip()
    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return jsonify({"error": "Server is not configured with WEATHER_API_KEY"}), 500

    try:
        response = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={"q": city, "appid": api_key, "units": "metric"},
            timeout=10,
        )
    except requests.RequestException:
        return jsonify({"error": "Failed to reach weather service"}), 502

    if response.status_code == 404:
        return jsonify({"error": "City not found"}), 404

    if response.status_code != 200:
        return jsonify({"error": "Weather service error"}), 502

    data = response.json()

    city_name = data.get("name") or city
    main = data.get("main", {})
    weather_list = data.get("weather", [])
    description = (weather_list[0].get("description") if weather_list else "").lower()
    temperature = main.get("temp")

    advice = _ai_advice(temperature, description, city_name) or _heuristic_advice(temperature, description)

    return jsonify(
        {
            "city": city_name,
            "temperature": temperature,
            "description": description,
            "advice": advice,
        }
    )
print("Time taken to fetch weather: ", dt.datetime.now() - start_time)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)



