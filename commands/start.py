from aiogram.types import Message, MessageEntity, MessageEntityType

from misc.scheduler import scheduler
from misc.send_info import send_info


async def start(msg: Message) -> None:
    async def scheduled_task() -> None:
        await send_info(msg)

    def add_job() -> None:
        scheduler.add_job(
            func=scheduled_task,
            trigger="cron",
            hour="8,20",
            id="main",
        )

    try:
        add_job()
    except:
        scheduler.remove_job(job_id="main")
        add_job()
    await send_info(msg)
    await msg.answer(text="Запущено")
