from dotenv import load_dotenv
import os

load_dotenv()

DB_USER = os.getenv("USER")
DB_PASSWORD = os.getenv("PASSWORD")
DB_HOST = os.getenv("HOST")
DB_PORT = os.getenv("PORT")
DB_NAME = os.getenv("DB") 