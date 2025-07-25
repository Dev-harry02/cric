from telegram.ext import CommandHandler, MessageHandler, filters
from db.mongo import db
import random
from utils.emoji import get_reaction

lobbies = {}

async def multiplayer(update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    if chat_id not in lobbies:
        lobbies[chat_id] = {
            "players": [user_id],
            "scores": {},
            "turn": 0,
            "state": "waiting"
        }
        await update.message.reply_text("🎮 Lobby created! Others can /joinmatch. Start with /startmatch.")
    else:
        await update.message.reply_text("⚠️ Lobby already exists.")

async def joinmatch(update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    lobby = lobbies.get(chat_id)

    if not lobby or lobby["state"] != "waiting":
        await update.message.reply_text("❌ No lobby to join.")
        return

    if user_id in lobby["players"]:
        await update.message.reply_text("You're already in the lobby.")
        return

    lobby["players"].append(user_id)
    await update.message.reply_text(f"✅ {update.effective_user.first_name} joined!")

async def startmatch(update, context):
    chat_id = update.effective_chat.id
    lobby = lobbies.get(chat_id)

    if not lobby or len(lobby["players"]) < 2:
        await update.message.reply_text("❌ Need at least 2 players.")
        return

    lobby["state"] = "playing"
    for uid in lobby["players"]:
        lobby["scores"][uid] = 0

    await prompt_turn(chat_id, context)

async def prompt_turn(chat_id, context):
    lobby = lobbies[chat_id]
    current_id = lobby["players"][lobby["turn"]]
    name = (await context.bot.get_chat(current_id)).first_name
    await context.bot.send_message(chat_id, text=f"🎯 {name}, it's your turn to BAT. Send a number (1-6).")

async def handle_multiplayer_input(update, context):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    msg = update.message.text.strip()
    lobby = lobbies.get(chat_id)

    if not lobby or lobby["state"] != "playing":
        return

    current_id = lobby["players"][lobby["turn"]]
    if user_id != current_id:
        return  # Not your turn

    if not msg.isdigit() or not (1 <= int(msg) <= 6):
        await update.message.reply_text("Enter a number (1-6).")
        return

    bat = int(msg)
    bowl = random.randint(1, 6)

    if bat == bowl:
        await update.message.reply_text(f"💥 OUT! Bot bowled {bowl}. Your total: {lobby['scores'][user_id]} runs.")
        db.history.insert_one({
            "user_id": user_id,
            "score": lobby["scores"][user_id],
            "mode": "multiplayer"
        })
        lobby["turn"] += 1
    else:
        lobby["scores"][user_id] += bat
        await update.message.reply_text(f"{get_reaction()} You hit {bat}! Bot bowled {bowl}. Total: {lobby['scores'][user_id]}")

    if lobby["turn"] >= len(lobby["players"]):
        result = "🏁 Match Over:
"
        for uid, score in lobby["scores"].items():
            name = (await context.bot.get_chat(uid)).first_name
            result += f"• {name}: {score} runs
"
        await context.bot.send_message(chat_id, result)
        del lobbies[chat_id]
    else:
        await prompt_turn(chat_id, context)

def register_multiplayer_handlers(app):
    app.add_handler(CommandHandler("multiplayer", multiplayer))
    app.add_handler(CommandHandler("joinmatch", joinmatch))
    app.add_handler(CommandHandler("startmatch", startmatch))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_multiplayer_input))