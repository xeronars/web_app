import psycopg
from psycopg import OperationalError

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