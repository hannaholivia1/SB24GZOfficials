import os
import json
import random
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ==================== SETUP ====================
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing in .env")

# Load content
def load_content():
    with open("content.json", "r", encoding="utf-8") as f:
        return json.load(f)

CONTENT = load_content()

# ==================== COMMANDS ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name or "friend"
    text = (
        f"👋 Hello {name}!\n\n"
        "Welcome to *SB24GZ Officials*.\n\n"
        "I share:\n"
        "• 💡 Daily useful tips\n"
        "• ⭐ Motivational quotes\n\n"
        "*Commands:*\n"
        "/tip – Get a tip\n"
        "/quote – Get a quote\n"
        "/about – About this bot\n"
        "/help – Show commands"
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def tip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(CONTENT["tips"]))

async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(CONTENT["quotes"]))

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(CONTENT["about"])

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📚 *Available Commands*\n\n"
        "/start – Welcome message\n"
        "/tip – Get a random tip\n"
        "/quote – Get a random quote\n"
        "/about – About this bot\n"
        "/help – Show this message"
    )
    await update.message.reply_text(text, parse_mode="Markdown")

# ==================== MAIN ====================
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tip", tip))
    app.add_handler(CommandHandler("quote", quote))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("help", help_cmd))

    print("🚀 SB24GZ Officials bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
