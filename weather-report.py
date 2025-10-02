import requests
import xml.etree.ElementTree as ET 
import json

URL_1 = "https://geocoding-api.open-meteo.com/v1/search"
URL_2 = "https://api.open-meteo.com/v1/forecast?current_weather=true"

response_1 = requests.get(URL_1)
print("Status:", response_1.status_code)
print("Final URL:", response_1.url)

response_2 = requests.get(URL_2)
print("Status:", response_2.status_code)
print("Final URL:", response_2.url)