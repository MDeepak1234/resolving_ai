
import os
from pathlib import Path
from dotenv import load_dotenv

# Get the project root directory
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")

# Groq configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "openai/gpt-oss-20b"

# Application configuration
APP_NAME = "AI Customer Support Assistant"

# Database configuration
DATABASE_PATH = BASE_DIR / "database" / "support.db"

# Vector database configuration
VECTORSTORE_PATH = BASE_DIR / "vectorstore"
DATA_PATH = BASE_DIR / "data"

# Validate API key
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing from the .env file")
