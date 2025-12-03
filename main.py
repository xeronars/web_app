import requests
import json
from weather_report import WeatherDB
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('db_name')
DB_USER = os.getenv('db_user')
DB_PASSWORD = os.getenv('db_password')
DB_HOST = os.getenv('db_host')
DB_PORT = os.getenv('db_port')

def fetch_weather(city, country, show_info=False):
    URL_1 = "https://geocoding-api.open-meteo.com/v1/search"
    params_1 = {"name": city, "country": country, "count": 1, "format": "json"}
    response_1 = requests.get(URL_1, params=params_1)
    if show_info:
        print("Status:", response_1.status_code)
        print("Final URL:", response_1.url)
    geo = response_1.json()["results"][0]
    lat, lon = geo["latitude"], geo["longitude"]

    URL_2 = "https://api.open-meteo.com/v1/forecast?current_weather=true"
    params_2 = {"latitude": lat, "longitude": lon, "current_weather": "true"}
    response_2 = requests.get(URL_2, params=params_2)
    if show_info:
        print("Status:", response_2.status_code)
        print("Final URL:", response_2.url)
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

    print(f"Weather in {city}, {country} is fetched successfully.")
    return data

def main():
    cities = [
        ("Chicago", "US"),
        ("Austin", "US"),
        ("New York", "US"),
        ("Los Angeles", "US"),
        ("Seattle", "US"),
        ("Denver", "US"),
        ("Miami", "US"),
        ("Boston", "US"),
        ("Dallas", "US"),
        ("San Francisco", "US")
        ]
    all_weather_data = []
    weather_db = WeatherDB(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)

    data = fetch_weather("Chicago", "US", show_info=True)
    all_weather_data.append(data)
    weather_db.insert_weather_report(data)

    for city, country in cities[1:]:
        data = fetch_weather(city, country)
        all_weather_data.append(data)
        weather_db.insert_weather_report(data)
    
    weather_db.read_weather_reports()
    weather_db.read_weather_report_by_id(3)
    weather_db.delete_weather_report(5)
    weather_db.read_weather_report_by_id(5)
    weather_db.update_weather_report_lat_lon(2, 40, -73)
    weather_db.read_weather_report_by_id(2)

    json_format = json.dumps(all_weather_data, indent=2)
    print("All weather data in JSON format:")
    print(json_format)
    
if __name__ == "__main__":
    main()
        
