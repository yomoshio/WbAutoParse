import asyncio
import logging
import os
from functools import partial

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from app.bot import handler
from app.api.v1.OpenAI import OpenAIApi

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
OPEN_AI_TOKEN = os.getenv("OPEN_AI_TOKEN")
PROXY_URL = os.getenv("PROXY_URL")

if not TOKEN:
    raise ValueError("❌ BOT_TOKEN is not set in .env")
if not OPEN_AI_TOKEN or not PROXY_URL:
    raise ValueError("❌ OPEN_AI_TOKEN or PROXY_URL missing in .env")

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=TOKEN)
    dp = Dispatcher()


    chat_gpt = OpenAIApi(key=OPEN_AI_TOKEN, proxy=PROXY_URL)

    handler.setup_handlers(dp, chat_gpt)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
