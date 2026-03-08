from __future__ import annotations

import logging
import os

try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
except Exception:  # pragma: no cover - optional dependency
    Update = None  # type: ignore
    Application = None  # type: ignore
    CommandHandler = None  # type: ignore
    ContextTypes = None  # type: ignore
    MessageHandler = None  # type: ignore
    filters = None  # type: ignore

from jarvis.brain.agent import JarvisAgent

logging.basicConfig(level=logging.INFO)


class JarvisTelegramBot:
    def __init__(self, agent: JarvisAgent) -> None:
        self.agent = agent
        self.token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.allowed_chat_id = os.getenv("TELEGRAM_CHAT_ID")

    async def _start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self._is_allowed(update):
            return
        await update.message.reply_text("JARVIS Telegram control online. Send a command.")

    async def _on_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self._is_allowed(update):
            return
        command = update.message.text or ""
        response = self.agent.execute_command(command)
        await update.message.reply_text(response[:4000])

    def _is_allowed(self, update: Update) -> bool:
        if not update.message:
            return False
        if not self.allowed_chat_id:
            return True
        return str(update.message.chat_id) == str(self.allowed_chat_id)

    def run(self) -> None:
        if Application is None:
            raise RuntimeError("python-telegram-bot is not installed.")
        if not self.token:
            raise ValueError("TELEGRAM_BOT_TOKEN is not set.")

        app = Application.builder().token(self.token).build()
        app.add_handler(CommandHandler("start", self._start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._on_message))
        app.run_polling()
