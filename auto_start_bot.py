import subprocess
import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
print("[DEBUG] BOT_TOKEN:", BOT_TOKEN)  # You can remove this after testing

PORT = 5000

def start_ngrok():
    print("[INFO] Starting Ngrok...")
    ngrok = subprocess.Popen(["ngrok", "http", str(PORT)], stdout=subprocess.DEVNULL)
    time.sleep(3)
    return ngrok

def get_ngrok_url():
    print("[INFO] Fetching Ngrok public URL...")
    try:
        response = requests.get("http://localhost:4040/api/tunnels")
        tunnels = response.json()["tunnels"]
        for tunnel in tunnels:
            if tunnel["proto"] == "https":
                url = tunnel["public_url"]
                print(f"[INFO] Ngrok URL: {url}")
                return url
        print("[ERROR] No HTTPS tunnel found.")
    except Exception as e:
        print("[ERROR] Could not fetch Ngrok URL:", e)
    return None

def start_flask_app():
    print("[INFO] Starting Flask bot (webhook_server.py)...")
    return subprocess.Popen(["python", "webhook_server.py"])

def wait_for_flask(url):
    print("[INFO] Waiting for Flask server to boot...")
    for _ in range(20):  # Try for up to 20 seconds
        try:
            resp = requests.get(f"{url}/webhook", headers={"ngrok-skip-browser-warning": "true"})
            if resp.status_code == 200:
                print("[INFO] Flask server is ready.")
                return True
        except:
            pass
        time.sleep(1)
    print("[ERROR] Flask did not respond in time.")
    return False

def set_webhook(ngrok_url):
    print("[INFO] Setting Telegram webhook...")
    webhook_url = f"{ngrok_url}/webhook"
    telegram_api = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    response = requests.post(telegram_api, data={"url": webhook_url})
    print("[RESPONSE] Telegram:", response.json())

if __name__ == "__main__":
    ngrok_process = start_ngrok()
    public_url = get_ngrok_url()

    if public_url:
        flask_process = start_flask_app()
        if wait_for_flask(public_url):
            set_webhook(public_url)
        else:
            print("[WARN] Webhook not set because Flask was not reachable.")
    else:
        print("[WARN] Ngrok URL not found — aborting.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[INFO] Shutting down...")
        ngrok_process.terminate()
        flask_process.terminate()
