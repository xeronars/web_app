import requests
import json
from weather_report import WeatherDB

DB_NAME = "web_app"
DB_USER = "postgres"                  
DB_PASSWORD = "Nguyenyennhi2!"           
DB_HOST = "localhost"                
DB_PORT = "5432"

def fetch_weather(city, country):
    URL_1 = "https://geocoding-api.open-meteo.com/v1/search"
    params_1 = {"name": city, "country": country, "count": 1, "format": "json"}

    response_1 = requests.get(URL_1, params=params_1)
    print("Status:", response_1.status_code)
    print("Final URL:", response_1.url)
    geo = response_1.json()["results"][0]
    lat, lon = geo["latitude"], geo["longitude"]

    URL_2 = "https://api.open-meteo.com/v1/forecast?current_weather=true"
    params_2 = {"latitude": lat, "longitude": lon, "current_weather": "true"}

    response_2 = requests.get(URL_2, params=params_2)
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
    json_format = json.dumps(data, indent=2)
    print(json_format)
    return data

def main():
    cities = [
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
    weather_db = WeatherDB(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)
    data = fetch_weather("Chicago", "US")
    weather_db.insert_weather_report(weather_db.conn, data)
    for city, country in cities:
        data = fetch_weather(city, country)
        weather_db.insert_weather_report(weather_db.conn, data)
    weather_db.read_weather_reports(weather_db.conn)
    weather_db.read_weather_report_by_id(weather_db.conn, 3)
    weather_db.delete_weather_report(weather_db.conn, 5)
    weather_db.read_weather_report_by_id(weather_db.conn, 2)
    weather_db.update_weather_report_lat_lon(weather_db.conn, 2, 40, -73)
    weather_db.read_weather_report_by_id(weather_db.conn, 2)
if __name__ == "__main__":
    main()
        
