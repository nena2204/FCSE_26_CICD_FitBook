import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://fitbook_user:fitbook_password@postgres:5432/fitbook_db"
)
DEBUG = os.getenv("DEBUG", "False") == "True"

