import os
import json
from datetime import datetime
from dotenv import load_dotenv
import httpx

# Optional: for future AI fallback
# from openai_fallback import get_openai_response
# from faq import check_faq

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
print("[DEBUG] BOT_TOKEN (bot.py):", BOT_TOKEN)

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN not found in .env")

# ✅ Send typing animation
async def send_typing(chat_id: int):
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{BASE_URL}/sendChatAction",
            json={"chat_id": chat_id, "action": "typing"}
        )

# ✅ Send text message
async def send_message(chat_id: int, text: str):
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/sendMessage", json=payload)
        print("📤 Sent to Telegram:", response.status_code, response.text)

# ✅ Send inline buttons
async def send_buttons(chat_id: int, message: str):
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "📄 View FAQs", "callback_data": "faq"},
                {"text": "🧠 Ask GPT", "callback_data": "gpt"}
            ],
            [
                {"text": "📞 Contact Support", "url": "https://t.me/amitsparky_bot"}
            ]
        ]
    }

    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown",
        "reply_markup": keyboard
    }

    async with httpx.AsyncClient() as client:
        await client.post(f"{BASE_URL}/sendMessage", json=payload)

# ✅ Save user query to file
def log_user_query(user_data, message):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_id": user_data.get("id"),
        "username": user_data.get("username"),
        "first_name": user_data.get("first_name"),
        "last_name": user_data.get("last_name"),
        "message": message
    }

    log_file = "user_queries.json"
    try:
        if os.path.exists(log_file):
            with open(log_file, "r+", encoding="utf-8") as file:
                data = json.load(file)
                data.append(log_entry)
                file.seek(0)
                json.dump(data, file, indent=2)
        else:
            with open(log_file, "w", encoding="utf-8") as file:
                json.dump([log_entry], file, indent=2)
    except Exception as e:
        print("❌ Error logging user query:", e)

# ✅ Process incoming updates
async def process_telegram_update(data: dict):
    try:
        if "message" in data:
            chat_id = data["message"]["chat"]["id"]
            user_data = data["message"]["from"]
            user_message = data["message"].get("text", "")

            if user_message:
                print(f"User: {user_message}")
                log_user_query(user_data, user_message)

                if user_message.lower() == "/start":
                    welcome = (
                        "👋 *Welcome to the Support Bot!*\n"
                        "_I can help you with FAQs or smart answers._"
                    )
                    await send_buttons(chat_id, welcome)
                    return

                if user_message.lower() == "/help":
                    help_text = (
                        "🛠 *Help Menu*\n"
                        "- Type your question\n"
                        "- Or use the buttons below"
                    )
                    await send_buttons(chat_id, help_text)
                    return

                # 🔁 Default reply path
                await send_typing(chat_id)

                # TEMP: Send a test reply instead of FAQ/OpenAI
                # faq_reply = check_faq(user_message)
                # if faq_reply:
                #     reply = faq_reply
                # else:
                #     reply = await get_openai_response(user_message)

                reply = "This is a test reply from *Sparky Bot*. 🤖"

                formatted_reply = f"📩 *Response:*\n_Hello! Thank you for your message._\n\n{reply}"
                await send_message(chat_id, formatted_reply)

        elif "callback_query" in data:
            callback = data["callback_query"]
            chat_id = callback["message"]["chat"]["id"]
            data_clicked = callback["data"]

            if data_clicked == "faq":
                await send_message(chat_id, "📄 *FAQ Tip:* Try asking: _'How do I reset my password?'_")
            elif data_clicked == "gpt":
                await send_message(chat_id, "🧠 *Smart Mode:* Type any question and I'll use AI to answer it.")

    except Exception as e:
        print("❌ Error in process_telegram_update:", e)
