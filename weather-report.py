import requests
import json
import psycopg
from psycopg import OperationalError

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

class WeatherDB:
    def __init__(self, dbname, user, password, host, port):
        try:
            self.conn = psycopg.connect(
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
            print("Connected to the database successfully.")
            self.create_table()
        except OperationalError as e:
            print(f"An error occurred while connecting to the database: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def create_table(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS weather_reports (
                    id SERIAL PRIMARY KEY,
                    city VARCHAR(100),
                    country VARCHAR(100),
                    latitude FLOAT,
                    longitude FLOAT,
                    temperature FLOAT,
                    windspeed_kmh FLOAT,
                    observation_time TIMESTAMP
                );
            """)
            self.conn.commit()
            print("Created weather_reports table.")

    def insert_weather_report(self, conn, data):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO weather_reports (city, country, latitude, longitude, temperature, windspeed_kmh, observation_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
                """,
                (data["city"], data["country"], data["latitude"], data["longitude"],
                 data["temperature"], data["windspeed_kmh"], data["observation_time"])
            )
            conn.commit()
            print(f"Weather report inserted.")

    def read_weather_reports(self, conn):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM weather_reports;")
            rows = cur.fetchall()
            print("Weather Reports:")
            for row in rows:
                print(row)

    def read_weather_report_by_id(self, conn, report_id):
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM weather_reports WHERE id = %s;", (report_id,))
            row = cur.fetchone()
            if row:
                print(f"Weather Report ID {report_id}: {row}")
            else:
                print(f"Cannot find ID: {report_id}.")

    def update_weather_report_lat_lon(self, conn, report_id, latitude, longitude):
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE weather_reports SET latitude = %s, longitude = %s WHERE id = %s;",
                (latitude, longitude, report_id)
            )
            conn.commit()
            print(f"Weather report with ID {report_id} updated.")
        

    def delete_weather_report(self, conn, report_id):
        with conn.cursor() as cur:
            cur.execute("DELETE FROM weather_reports WHERE id = %s;", (report_id,))
            conn.commit()
            print(f"Deleted weather report with ID {report_id}.")

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
        
