# main.py
import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from faq import check_faq
from openai_fallback import get_openai_response

# Load .env variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# === Reply Formatter ===
def format_reply(reply):
    return (
        "📩 *Response:*\n_Hello! Thank you for your message._\n\n" + reply
    )


# === /start Command ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [
            InlineKeyboardButton("📄 View FAQs", callback_data="faq"),
            InlineKeyboardButton("🧠 Ask GPT", callback_data="gpt"),
        ],
        [
            InlineKeyboardButton("📞 Contact Support", url="https://t.me/amitsparky_bot")
        ],
    ]
    await update.message.reply_text(
        "👋 *Welcome to the Support Bot!*\n_I can help you with FAQs or smart answers._",
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="Markdown",
    )


# === /help Command ===
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛠 *Help Menu*\n- Type your question\n- Or use the buttons below",
        parse_mode="Markdown",
    )


# === Main Text Message Handler ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    user = update.message.from_user
    chat_id = update.message.chat.id

    log_user_query(user, message)

    await context.bot.send_chat_action(chat_id=chat_id, action="typing")

    reply = check_faq(message)
    if not reply:
        try:
            reply = await get_openai_response(message)
        except Exception as e:
            logging.error(f"OpenAI error: {e}")
            reply = "I'm sorry, I couldn't generate a smart reply right now."

    await update.message.reply_text(format_reply(reply), parse_mode="Markdown")


# === Inline Button Handler ===
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat.id

    if query.data == "faq":
        await context.bot.send_message(
            chat_id=chat_id,
            text="📄 *FAQ Tip:* Try asking: _'How do I reset my password?'_",
            parse_mode="Markdown",
        )
    elif query.data == "gpt":
        await context.bot.send_message(
            chat_id=chat_id,
            text="🧠 *Smart Mode:* Type any question and I'll use AI to answer it.",
            parse_mode="Markdown",
        )


# === Log User Messages ===
def log_user_query(user, message):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "user_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "message": message,
    }

    log_file = "user_queries.json"
    try:
        if os.path.exists(log_file):
            with open(log_file, "r+", encoding="utf-8") as f:
                data = json.load(f)
                data.append(entry)
                f.seek(0)
                json.dump(data, f, indent=2)
        else:
            with open(log_file, "w", encoding="utf-8") as f:
                json.dump([entry], f, indent=2)
    except Exception as e:
        logging.error(f"Logging error: {e}")


# === Start the Bot ===
if __name__ == "__main__":
    if not BOT_TOKEN:
        raise ValueError("❌ BOT_TOKEN not set in .env file")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🚀 Bot is running... Press CTRL+C to stop.")
    app.run_polling()
