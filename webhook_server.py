from flask import Flask, request
import asyncio
from bot import process_telegram_update

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        print("✅ Webhook received:", data)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(process_telegram_update(data))
    except Exception as e:
        print("❌ Error in webhook:", e)
    return "ok", 200

@app.route('/')
def index():
    return "🤖 Hello! Flask bot is running!"

@app.route('/webhook', methods=['GET'])  # Optional GET route
def debug_webhook():
    return "✅ GET /webhook works", 200

if __name__ == '__main__':
    print("🚀 Starting Flask server...")
    app.run(host='0.0.0.0', port=5000)
