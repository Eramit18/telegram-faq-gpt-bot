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

# Load environment variables from .env
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# === Format the Bot Reply ===
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

    await update.
