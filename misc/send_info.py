from typing import Union

from aiogram import Dispatcher
from aiogram.types import Message

from binance import get_currencies
from binance.currency_model import Coins
from envars import CHANNEL_ID


async def send_info(msg: Union[Message, Dispatcher]):
    resp = await get_currencies.bulk_get()
    with open("data/pics/digest.jpg", "rb") as f:
        await msg.bot.send_photo(chat_id=CHANNEL_ID, photo=f, caption=Coins(resp).list_all())
