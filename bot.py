# ============ HIDE TOKEN FROM LOGS ============
import logging
logging.getLogger("httpx").setLevel(logging.WARNING)

import os
import json
import random
import asyncio
import threading
from html import escape
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN set!")

# ============ LOAD CONTENT ============
def load_content():
    try:
        with open("content.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading content.json: {e}")
        return {"tips": ["Stay consistent."], "quotes": ["Keep going."], "about": "SB24GZ Officials bot."}

CONTENT = load_content()

# ============ FLASK - KEEPS HOST ALIVE ============
flask_app = Flask(__name__)

@flask_app.route("/")
def health_check():
    return "SB24GZ Officials bot is running!", 200

# ============ COMMANDS ============
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = escape(update.effective_user.first_name or "friend")
    text = (
        f"👋 Hello {name}!\n\n"
        "Welcome to <b>SB24GZ Officials</b>.\n\n"
        "I share:\n"
        "• 💡 Daily useful tips\n"
        "• ⭐ Motivational quotes\n\n"
        "<b>Commands:</b>\n"
        "/tip - Get a tip\n"
        "/quote - Get a quote\n"
        "/about - About this bot\n"
        "/help - Show commands"
    )
    await update.message.reply_text(text, parse_mode="HTML")

async def tip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(CONTENT["tips"]))

async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(CONTENT["quotes"]))

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(CONTENT["about"])

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📚 <b>Available Commands</b>\n\n"
        "/start - Welcome message\n"
        "/tip - Get a random tip\n"
        "/quote - Get a random quote\n"
        "/about - About this bot\n"
        "/help - Show this message"
    )
    await update.message.reply_text(text, parse_mode="HTML")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")

# ============ BOT STARTUP ============
async def run_bot_async():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tip", tip))
    app.add_handler(CommandHandler("quote", quote))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_error_handler(error_handler)

    await app.initialize()
    await app.start()
    await app.updater.start_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )
    logger.info("SB24GZ Officials bot is polling and ready!")
    while True:
        await asyncio.sleep(1)

def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_bot_async())

bot_thread = threading.Thread(target=run_bot, daemon=True)
bot_thread.start()
