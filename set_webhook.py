import requests
import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Make sure your .env file has this
NGROK_URL = "https://6b64-2401-4900-884a-9687-65ff-f5d3-553a-e614.ngrok-free.app/webhook"

webhook_url = f"{NGROK_URL}/webhook"

response = requests.get(
    f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook",
    params={"url": webhook_url}
)

print("📡 Telegram response:", response.json())
