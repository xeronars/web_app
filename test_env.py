import os
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env file

username = os.getenv('db_user')
password = os.getenv("db_password")
database_url = os.getenv("DATABASE_URL")