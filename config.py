import os
from dotenv import load_dotenv

# Load local environment variables if present
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", "8000"))
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Strict startup assertion check
if not BOT_TOKEN:
    raise ValueError("CRITICAL FAILURE: The BOT_TOKEN environment variable is missing!")
if not WEBHOOK_URL:
    raise ValueError("CRITICAL FAILURE: The WEBHOOK_URL environment variable is missing!")
