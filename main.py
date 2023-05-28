import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils.executor import start_webhook

import commands
import envars as env
from misc.scheduler import scheduler
from misc.send_info import send_info


# Main function
def main() -> None:
    """
    Bots 'Heart'

    Setups core-functionality
    """
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=env.API_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())

    dp.middleware.setup(LoggingMiddleware())

    async def on_startup(self):
        """
        Webhook startup
        """

        logging.warning("Starting webhook...")
        commands.setup(dp)
        logging.info("Preparing DB...")
        logging.info("DB set!")
        scheduler.start()
        # Check webhook url
        webhook = await bot.get_webhook_info()
        if webhook.url != env.WEBHOOK_URL:
            logging.warning(f"Bad webhook url: {webhook.url}, resolving...")
            if not webhook.url:
                await bot.delete_webhook()
                logging.warning("Webhook url deleted")
            await bot.set_webhook(
                env.WEBHOOK_URL,
                allowed_updates=[
                    "message",
                    "callback_query",
                    "chat_member",
                    "my_chat_member",
                ],
            )
            logging.warning("Set new webhook url")

        async def scheduled_task():
            await send_info(dp)

        scheduler.add_job(
            func=scheduled_task,
            trigger="cron",
            hour="8,20",
            id="main",
        )

    async def on_shutdown(self):
        """
        Actions to perform on WebHook Shutdown

        Note: self.delete_webhook() is not used due to startrup issues
        When running on hosting
        """
        logging.warning("shutting down...")
        logging.warning("Bye!")

    start_webhook(
        dispatcher=dp,
        webhook_path=env.WEBHOOK_URL_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=env.WEBAPP_HOST,
        port=env.WEBAPP_PORT,
    )


if __name__ == "__main__":
    main()
