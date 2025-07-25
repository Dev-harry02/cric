from telegram.ext import CommandHandler
from db.mongo import db

async def start(update, context):
    await update.message.reply_text("🏏 Welcome to the Telegram Cricket Bot!
Use /help to get started.")

async def help_command(update, context):
    await update.message.reply_text("""
📘 *Cricket Bot Commands*:
- /solo – Start a solo match
- /multiplayer – Create group match
- /joinmatch – Join an existing match
- /startmatch – Begin the match
- /score – Show your scores
- /teamcreate <name> – Create a team
- /teamjoin <name> – Join a team
- /teamlist – List all teams
- /rules – Game rules
- /resetteams – (Admin) Reset all teams
- /resetmatches – (Admin) Clear match history
    """, parse_mode='Markdown')

async def rules(update, context):
    await update.message.reply_text("""
📜 *Game Rules*:
- Choose 1–6 to bat or bowl
- If your number = opponent's, you're OUT!
- Score as many as possible
- Turn-based matches in group chats
    """, parse_mode='Markdown')

async def resetteams(update, context):
    if update.effective_user.id not in [admin.id async for admin in update.effective_chat.get_administrators()]:
        await update.message.reply_text("❌ Admins only.")
        return
    db.teams.delete_many({})
    await update.message.reply_text("✅ All teams reset.")

async def resetmatches(update, context):
    if update.effective_user.id not in [admin.id async for admin in update.effective_chat.get_administrators()]:
        await update.message.reply_text("❌ Admins only.")
        return
    db.history.delete_many({})
    await update.message.reply_text("✅ Match history cleared.")

def register_core_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("rules", rules))
    app.add_handler(CommandHandler("resetteams", resetteams))
    app.add_handler(CommandHandler("resetmatches", resetmatches))