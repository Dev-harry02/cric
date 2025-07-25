from telegram.ext import CommandHandler
from db.mongo import db

async def teamcreate(update, context):
    if not context.args:
        await update.message.reply_text("Usage: /teamcreate <team_name>")
        return
    team_name = " ".join(context.args)
    user_id = update.effective_user.id
    existing = db.teams.find_one({"name": team_name})
    if existing:
        await update.message.reply_text("❌ Team already exists.")
        return
    db.teams.insert_one({"name": team_name, "members": [user_id]})
    await update.message.reply_text(f"✅ Team '{team_name}' created and you joined it.")

async def teamjoin(update, context):
    if not context.args:
        await update.message.reply_text("Usage: /teamjoin <team_name>")
        return
    team_name = " ".join(context.args)
    user_id = update.effective_user.id
    team = db.teams.find_one({"name": team_name})
    if not team:
        await update.message.reply_text("❌ Team not found.")
        return
    if user_id in team["members"]:
        await update.message.reply_text("⚠️ You're already in the team.")
        return
    db.teams.update_one({"name": team_name}, {"$push": {"members": user_id}})
    await update.message.reply_text(f"✅ Joined team '{team_name}'.")

async def teamlist(update, context):
    teams = db.teams.find()
    text = "📋 *Teams List:*

"
    for team in teams:
        text += f"🔹 {team['name']} ({len(team['members'])} members)
"
    await update.message.reply_text(text or "No teams yet.", parse_mode="Markdown")

def register_team_handlers(app):
    app.add_handler(CommandHandler("teamcreate", teamcreate))
    app.add_handler(CommandHandler("teamjoin", teamjoin))
    app.add_handler(CommandHandler("teamlist", teamlist))