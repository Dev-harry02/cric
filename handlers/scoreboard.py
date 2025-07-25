from telegram.ext import CommandHandler
from db.mongo import db

async def score(update, context):
    user_id = update.effective_user.id
    games = db.history.find({"user_id": user_id}).sort("score", -1).limit(5)
    text = "🏏 Your Top Scores:
"
    for g in games:
        text += f"• {g['score']} runs (mode: {g['mode']})
"
    await update.message.reply_text(text or "No scores yet.")

async def history(update, context):
    user_id = update.effective_user.id
    games = db.history.find({"user_id": user_id}).sort("_id", -1).limit(5)
    text = "🕘 Last 5 Matches:
"
    for g in games:
        text += f"• {g['score']} runs ({g['mode']})
"
    await update.message.reply_text(text or "No history yet.")

def register_scoreboard_handlers(app):
    app.add_handler(CommandHandler("score", score))
    app.add_handler(CommandHandler("history", history))