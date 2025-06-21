import os
from dotenv import load_dotenv
from fastapi import FastAPI

# Load .env two levels up
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../.env'))
print(f"DEBUG: main.py is trying to load .env from: {dotenv_path}")
load_dotenv(dotenv_path)

db_url_from_env = os.getenv("DATABASE_URL")
if db_url_from_env:
    print(f"DEBUG: DATABASE_URL successfully loaded from .env: {db_url_from_env}")
else:
    print("DEBUG: DATABASE_URL NOT FOUND when loading .env manually.")

from src.routes import auth, contact

app = FastAPI()

app.include_router(auth.router, prefix="/api/auth")
app.include_router(contact.router, prefix="/api/contacts")