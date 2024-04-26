import asyncio
import os
import logging
from aiogram import Bot, Dispatcher
from app.handlers import router
from dotenv import load_dotenv

async def main():
    load_dotenv()
    TOKEN = os.getenv("TOKEN")
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    finally:
        print("Exiting")