import asyncio

import aiohttp


async def fetch(session: aiohttp.ClientSession, coin_pair):
    async with session.get(f"https://api.binance.com/api/v3/ticker/24hr?symbol={coin_pair}") as r:
        if r.raise_for_status != 200:
            r.raise_for_status()
        return await r.json()


async def bulk_fetch(session: aiohttp.ClientSession, coins):
    async with session.get(f"https://api.binance.com/api/v3/ticker/24hr?symbols={coins}") as r:
        if r.raise_for_status != 200:
            r.raise_for_status()
        # print(r.text())
        return await r.json()


async def bulk_get():
    coins = [
        "BTCUSDT",
        "ETHUSDT",
        "BNBUSDT",
        "ADAUSDT",
        "CFXUSDT",
        "GMTUSDT",
        "SOLUSDT",
        "TRXUSDT",
        "DASHUSDT",
        "XRPUSDT",
    ]
    async with aiohttp.ClientSession() as s:
        cc = f"""[\"{'","'.join(coins)}\"]"""
        return await bulk_fetch(s, cc)


async def fetch_all(session: aiohttp.ClientSession, coins):
    tasks = []
    for coin in coins:
        tasks.append(asyncio.create_task(fetch(session, coin)))
    res = await asyncio.gather(*tasks)
    return res


async def get():
    coins = [
        "BTCUSDT",
        "ETHUSDT",
        "BNBUSDT",
        "ADAUSDT",
        "CFXUSDT",
        "GMTUSDT",
        "SOLUSDT",
        "TRXUSDT",
        "DASHUSDT",
        "XRPUSDT",
    ]
    coin_p = ["[%22BTCUSDT%22,%22ETHUSDT%22]"]
    async with aiohttp.ClientSession() as s:
        return await fetch_all(s, coins)
        # print(requests)
        # print(Coins(requests).list_all())
