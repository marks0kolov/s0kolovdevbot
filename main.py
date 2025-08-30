import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from handlers import masterR, idR, infoR
from config import BOT_TOKEN, PARSE_MODE

bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=PARSE_MODE))
dp = Dispatcher()

########################### - MAIN - ###########################

async def main():
    # include all routers:
    dp.include_router(idR)
    dp.include_router(infoR)
    dp.include_router(masterR)

    await dp.start_polling(bot) # start bot polling

asyncio.run(main())