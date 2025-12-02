# Weather Reporter
A combination of Flask web application and Python that fetches real-time weather data from Open API and stores them in a PostgreSQL database. Web application also allows user to insert the city name and view the data.

## Features
1. Weather data fetching
    - Get weather data from Open API (temp, windspeed, timespamp)
2. PostgreSQL database
    - Create a table if not exist.
    - Included usages:
        - Inserting weather report data.
        - Sort data by ID.
        - Updating longtitude/latitude.
        - Deleting data.
        - View all saved data in the database through the website UI.
3. Flask
    - Simplified UI asking the user to enter a city name.
    - Print out the result if the city name is correct and is inside the database.
    - "View all reports" button to show the list of saved reports, gotten from PostgreSQL database.

## Installation
1. Clone the repository
```bash
git clone https://github.com/xeronars/web_app.git
cd weather_report
```

2. After cloning, create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate      # use this if Mac/Linux
.venv\Scripts\activate        # use this if Windows
```

3. Install dependencies for libs
```bash
pip install -r requirements.txt
```

4. Create a .env file to store private information

Put these into your .env file:

```bash
db_name=your_database
db_user=your_username
db_password=your_password
db_host=localhost
db_port=5432
```

5. Setting up PostgreSQL to store data
```sql
CREATE DATABASE weather_db;
```
The table for the data will be created by the program in weather_report.py and main.py

```pgsql
weather_reports (
    id SERIAL PRIMARY KEY,
    city VARCHAR(100),
    country VARCHAR(100),
    latitude FLOAT,
    longitude FLOAT,
    temperature FLOAT,
    windspeed_kmh FLOAT,
    observation_time TIMESTAMP
)
```
6. Running the Flask website

*Do NOT run the project using the “Go Live” button in Visual Studio Code.*

Run this in your terminal to start the Flask server:

```bash
python app.py
```

Then, open the website in your browser:

```cpp
http://127.0.0.1:5000
```


## Requirements
- *Python 3.13.9*
- *PostgreSQL 13+*
- *pip (newest version)*
- *Virtual environment (.venv)*

## Structure
```text
project/
├── app.py                 # Flask 
├── main.py                # Weather fetching script
├── weather_report.py      # PostgreSQL database connecting and executing commands
├── templates/
│   ├── home.html
│   ├── result.html
│   └── viewall.html
├── requirements.txt
├── .env                   
└── README.md
```
