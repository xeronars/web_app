import psycopg
from psycopg import OperationalError


class WeatherDB:
    """
    Class to handle PostgreSQL database operations for weather reports.
    
    Attributes:
        conn: psycopg.Connection: Connection object to the PostgreSQL database.
    """
    def __init__(self, dbname, user, password, host, port):
        """
        Initialize instance and connect to the PostgreSQL database.

        Args:
            dbname (str): Name of the database.
            user (str): Database user.
            password (str): Password for the database user.
            host (str): Host address of the database.
            port (str): Port number for the database connection.
        """
        try:
            self.conn = psycopg.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            print("Connected to the database successfully.")
            self.create_table()
        except OperationalError as e:
            print(f"An error occurred while connecting to the database: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def create_table(self):
        """
        Create the weather_reports table if it does not exist.
        """
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

    def insert_weather_report(self, data):
        """
        Insert a new weather report data into the weather_reports table.

        Args:
            data (dict): A dictionary containing:
                         city, country, latitude, longitude, temperature,
                         windspeed_kmh, observation_time.
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO weather_reports (city, country, latitude, longitude, temperature, windspeed_kmh, observation_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
                """,
                (data["city"], data["country"], data["latitude"], data["longitude"],
                 data["temperature"], data["windspeed_kmh"], data["observation_time"])
            )
            self.conn.commit()
            print(f"Weather report inserted.")

    def read_weather_reports(self):
        """
        Read and print all weather reports from the weather_reports table.
        """
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM weather_reports;")
            rows = cur.fetchall()
            print("Weather Reports:")
            for row in rows:
                print(row)

    def read_weather_report_by_id(self, report_id):
        """
        Read and print a weather report by its ID.
        Args:
            report_id (int): ID of the weather report to retrieve and display.
        """
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM weather_reports WHERE id = %s;", (report_id,))
            row = cur.fetchone()
            if row:
                print(f"Weather Report ID {report_id}: {row}")
            else:
                print(f"Cannot find ID: {report_id}.")

    def update_weather_report_lat_lon(self, report_id, latitude, longitude):
        """
        Update the latitude and longitude of a weather report by its ID.

        Args:
            report_id (int): ID of the weather report to update.
            latitude (float): new latitude.
            longitude (float): new longitude.
        """
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE weather_reports SET latitude = %s, longitude = %s WHERE id = %s;",
                (latitude, longitude, report_id)
            )
            self.conn.commit()
            print(f"Weather report with ID {report_id} updated.")
        

    def delete_weather_report(self, report_id):
        """
        Delete a weather report by its ID.
        Args:
            report_id (int): ID of the weather report to delete.
        """
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM weather_reports WHERE id = %s;", (report_id,))
            self.conn.commit()
            print(f"Deleted weather report with ID {report_id}.")