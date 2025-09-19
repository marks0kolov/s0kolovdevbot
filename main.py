import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage


from handlers import masterR, idR, infoR, userR
from config import BOT_TOKEN, PARSE_MODE

storage = MemoryStorage()

bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=PARSE_MODE))
dp = Dispatcher(storage=storage)

########################### - MAIN - ###########################

async def main():
    # include all routers:
    dp.include_router(idR)
    dp.include_router(infoR)
    dp.include_router(masterR)
    dp.include_router(userR)

    await dp.start_polling(bot) # start bot polling

asyncio.run(main())