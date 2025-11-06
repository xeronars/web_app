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

def create_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS weather_reports (
                id SERIAL PRIMARY KEY,
                city VARCHAR(100),
                country VARCHAR(10),
                latitude FLOAT,
                longitude FLOAT,
                temperature FLOAT,
                windspeed_kmh FLOAT,
                observation_time TIMESTAMP,
                notes TEXT
            );
        """)
        conn.commit()
        print("Table 'weather_reports' is ready.")

def insert_weather_report(conn, report):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO weather_reports (city, country, latitude, longitude, temperature, windspeed_kmh, observation_time)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (
            report["city"],
            report["country"],
            report["latitude"],
            report["longitude"],
            report["temperature"],
            report["windspeed_kmh"],
            report["observation_time"]
        ))
        conn.commit()
        print(f"Weather report for {report['city']}, {report['country']} inserted successfully.")

def read_weather_reports(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM weather_reports;")
        rows = cur.fetchall()
        print("Weather Reports:")
        for row in rows:
            print(row)

def update_weather_report(conn, report_id, new_notes):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE weather_reports
            SET notes = %s
            WHERE id = %s;
        """, (new_notes, report_id))
        conn.commit()
        print(f"Weather report's note with ID {report_id} updated successfully.")

def delete_weather_report(conn, report_id):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM weather_reports WHERE id = %s;", (report_id,))
        conn.commit()
        print(f"Weather report with ID {report_id} deleted successfully.")

def main():
    try:
        with psycopg.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        ) as conn:
            print("Connected to the database successfully.")

            create_table(conn)

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

            for city, country in cities:
                data = fetch_weather(city, country)
                insert_weather_report(conn, data)

            read_weather_reports(conn)

            update_weather_report(conn, 1, "Chilly weather, wear a coat!")
            delete_weather_report(conn, 2)

            read_weather_reports(conn)
    
    except OperationalError as e:
        print(f"An error occurred while connecting to the database: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
        
