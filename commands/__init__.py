from aiogram import Dispatcher

from middleware.processor import ProcessorMiddleware

from .start import start
from .tools.admin_handler import admin, admin_only


def setup(dp: Dispatcher) -> None:
    dp.middleware.setup(ProcessorMiddleware())
    # dp.register_message_handler(admin, admin_only, commands=["start"])
    dp.register_message_handler(start, commands=["start"])
