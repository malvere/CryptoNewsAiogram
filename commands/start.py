from aiogram.types import Message

from binance import get_currencies
from binance.currency_model import Coins
from envars import CHANNEL_ID
from misc.send_info import send_info


async def start(msg: Message) -> None:
    await send_info(msg)
