import logging
from aiogram import Bot, Dispatcher
from app.config import BOT_TOKEN
from app.handlers.menu import router as menu_router
from app.handlers.services import router as services_router
from app.handlers.mult_table import router as mult_table_router
from app.handlers.online import router as online_router

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp.include_router(menu_router)
dp.include_router(services_router)
dp.include_router(mult_table_router)
dp.include_router(online_router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())