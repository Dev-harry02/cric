from telegram.ext import MessageHandler, CommandHandler, filters
from db.mongo import db
import random
from utils.emoji import get_reaction

solo_games = {}

async def solo(update, context):
    user_id = update.effective_user.id
    solo_games[user_id] = {"score": 0, "active": True}
    await update.message.reply_text("🎮 Solo Match Started! Send a number (1-6) to bat!")

async def handle_solo_input(update, context):
    user_id = update.effective_user.id
    msg = update.message.text.strip()

    if user_id not in solo_games or not solo_games[user_id]["active"]:
        return

    if not msg.isdigit() or not (1 <= int(msg) <= 6):
        await update.message.reply_text("❌ Please enter a valid number between 1 and 6.")
        return

    bat = int(msg)
    bowl = random.randint(1, 6)
    if bat == bowl:
        score = solo_games[user_id]["score"]
        solo_games[user_id]["active"] = False
        db.history.insert_one({"user_id": user_id, "score": score, "mode": "solo"})
        await update.message.reply_text(f"💥 You're OUT! Bot bowled {bowl}. Total: {score} runs.")
    else:
        solo_games[user_id]["score"] += bat
        await update.message.reply_text(f"{get_reaction()} You scored {bat} (Bot: {bowl}) | Total: {solo_games[user_id]['score']}")

def register_solo_handlers(app):
    app.add_handler(CommandHandler("solo", solo))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_solo_input))