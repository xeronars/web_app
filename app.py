from flask import Flask, request, jsonify
from weather_report import WeatherDB
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

@app.route("/")
def home():
    return "Welcome to the Weather Report!"

@app.route("/report", methods=["GET"])
def get_weather_report():
    with weather_db.conn as cur:
        cur.execute("SELECT * FROM weather_reports;")
