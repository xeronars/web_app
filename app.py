from flask import Flask, request, jsonify, render_template
from weather_report import WeatherDB
import requests
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('db_name')
DB_USER = os.getenv('db_user')
DB_PASSWORD = os.getenv('db_password')
DB_HOST = os.getenv('db_host')
DB_PORT = os.getenv('db_port')

app = Flask(__name__)

weather_db = WeatherDB(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)

def fetch_weather(city, country="US"):
    URL_1 = "https://geocoding-api.open-meteo.com/v1/search"
    params_1 = {"name": city, "country": country, "count": 1, "format": "json"}
    response_1 = requests.get(URL_1, params=params_1)

    geo = response_1.json()["results"][0]
    lat, lon = geo["latitude"], geo["longitude"]

    URL_2 = "https://api.open-meteo.com/v1/forecast"
    params_2 = {"latitude": lat, "longitude": lon, "current_weather": "true"}
    response_2 = requests.get(URL_2, params=params_2)

    weather = response_2.json()["current_weather"]

    data = {
        "city": geo["name"],
        "country": geo["country_code"],
        "latitude": lat,
        "longitude": lon,
        "temperature": weather["temperature"],
        "windspeed_kmh": weather["windspeed"],
        "observation_time": weather["time"],
    }
    return data

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/result", methods=["GET", "POST"])
def result():
    if request.method == "POST":
        city = request.form.get("city")
        if not city:
            return "City not provided", 400
        data = fetch_weather(city)
        if data:
            weather_db.insert_weather_report(data)
            return render_template("result.html", weather=data)
        else:
            return "City not found or API error", 404
    return render_template("home.html") 

@app.route("/viewall")
def viewall():
    with weather_db.conn.cursor() as cur: 
        cur.execute("SELECT * FROM weather_reports;") 
        rows = cur.fetchall() 
    return render_template("viewall.html", rows=rows)  


if __name__ == "__main__":
    app.run(debug=True)
