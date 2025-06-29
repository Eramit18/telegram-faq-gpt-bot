import os
import subprocess
import time
import requests
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_PATH = "/webhook"
NGROK_PORT = 5000

def get_public_url():
    time.sleep(3)  # Give ngrok time to initialize
    try:
        response = requests.get("http://127.0.0.1:4040/api/tunnels")
        tunnels = response.json()["tunnels"]
        for tunnel in tunnels:
            if tunnel["proto"] == "https":
                return tunnel["public_url"]
    except Exception as e:
        print("❌ Failed to get ngrok URL:", e)
    return None

def set_telegram_webhook(public_url):
    full_url = f"{public_url}{WEBHOOK_PATH}"
    print(f"📬 Full webhook URL: {full_url}")  # ✅ Clean enhancement
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    response = requests.post(url, json={"url": full_url})
    print("📡 Webhook Set:", response.json())

if __name__ == "__main__":
    print("🚀 Starting ngrok tunnel...")
    subprocess.Popen(["ngrok", "http", str(NGROK_PORT)])

    public_url = None
    for _ in range(10):
        public_url = get_public_url()
        if public_url:
            break
        time.sleep(1)

    if public_url:
        print(f"🌍 Public URL: {public_url}")
        set_telegram_webhook(public_url)
    else:
        print("❌ Could not detect public URL. Is ngrok running?")
