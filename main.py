from telegram.ext import ApplicationBuilder
from handlers.core import register_core_handlers
from handlers.solo import register_solo_handlers
from handlers.multiplayer import register_multiplayer_handlers
from handlers.scoreboard import register_scoreboard_handlers
from handlers.teams import register_team_handlers
from db.mongo import init_db

import config

def main():
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()

    init_db()

    # Register handlers
    register_core_handlers(app)
    register_solo_handlers(app)
    register_multiplayer_handlers(app)
    register_scoreboard_handlers(app)
    register_team_handlers(app)

    print("🏏 Cricket Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()