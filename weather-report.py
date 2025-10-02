import requests
import json

URL_1 = "https://geocoding-api.open-meteo.com/v1/search"
#params_1 = {"name": "Chicago", "country": "US", "count": 1, "format": "json"}
params_1 = {"name": "Austin", "country": "US", "count": 1, "format": "json"}

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
    "latitude": lat,
    "longitude": lon,
    "temperature": weather["temperature"],
    "windspeed_kmh": weather["windspeed"],
    "observation_time": weather["time"],
    }

json_format = json.dumps(data, indent=2)
print(json_format)
