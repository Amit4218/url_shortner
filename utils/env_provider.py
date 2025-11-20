from dotenv import load_dotenv
import os

load_dotenv()

HOST_URL = os.getenv("HOST_URL")

DATABASE_URL = os.getenv("DATABASE_URL")
