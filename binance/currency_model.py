class Coin(object):
    def __init__(self, **kwargs) -> None:
        self.symbol = kwargs["symbol"][:-4]
        self.priceChangePercent = kwargs["priceChangePercent"].rstrip("0")
        self.lastPrice = kwargs["lastPrice"].rstrip("0")
        self.volume = kwargs["volume"].rstrip("0")

    def list_all(self, **kwargs):
        for arg, value in kwargs:
            print(f"{arg}: {value}")

    def __str__(self) -> str:
        if "-" in self.priceChangePercent:
            indicator = "📉"
        else:
            indicator = "📈"
        return f"""
            {indicator} ${self.symbol}: {self.lastPrice} ({self.priceChangePercent}%)
        """.strip()


class Coins(object):
    def __init__(self, coins: list) -> None:
        self.coins = coins

    def _market_cap(self, coin: Coin):
        cap = float(coin.volume) * float(coin.lastPrice) * 10 ** (-9)
        return f"{str(cap)[:5]}B"

    def list_all(self):
        btc = Coin(**next((item for item in self.coins if item["symbol"] == "BTCUSDT")))
        info = ""
        for coin in self.coins:
            info += f"{Coin(**coin).__str__()}\n"
        return f"Доброго времени суток и продуктивного дня!\n{info} \n 💸 Капитализация: {self._market_cap(btc)} \n 📊Объём торгов: {btc.volume} \n\n @DigitalTradingRoom"
