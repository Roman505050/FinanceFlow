from dotenv import load_dotenv
import os

load_dotenv()

# Load environment variables
POSTGRES_URI = os.getenv(
    "POSTGRES_URI",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres",
)
SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY", "super secret key")
