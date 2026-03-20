import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Define single instance variables here from .env
NEXT_ACTION_ID = os.getenv("NEXT_ACTION_ID")
COOKIE = os.getenv("COOKIE")
DATA_FILE_PATH = Path(os.getenv("DATA_FILE"))