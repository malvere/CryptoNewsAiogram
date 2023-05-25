import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import commands
import envars as env
from misc.scheduler import scheduler


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=env.API_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())
    commands.setup(dp)
    try:
        from misc.send_info import send_info

        async def scheduled_task():
            await send_info(dp)

        scheduler.start()
        scheduler.add_job(
            func=scheduled_task,
            trigger="cron",
            hour="8-20",
        )

        await bot.delete_webhook()
        await bot.get_updates()
        await dp.start_polling(
            allowed_updates=[
                "message",
                "callback_query",
                "chat_member",
                "my_chat_member",
            ]
        )
    finally:
        # await bot.close()
        pass


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Goodbye!")
