import asyncio
from time import sleep, time
from price import get_current_value_price
import threading
import ccxt
import numpy as np
from sklearn.linear_model import LinearRegression


class Detection:

    def __init__(self):
        super().__init__()
        self.exchange = ccxt.binance()
        self.TIME_FOR_WAIT_IN_SECOND: int = 3600
        self.time_ETHUSDT: list = []
        self.price_ETHUSDT: list = []
        self.current_time: float = 0
        self.timer = time()

    async def check_change_price(self):

        while True:
            self.current_time = time()
            current_price = await get_current_value_price(self.exchange)
            self.time_ETHUSDT.append(self.current_time)
            self.price_ETHUSDT.append(current_price)
            if len(self.time_ETHUSDT) >= 2 and self.current_time - self.timer > self.TIME_FOR_WAIT_IN_SECOND:
                self.timer = self.current_time
                x = np.array(self.time_ETHUSDT).reshape((len(self.time_ETHUSDT), 1))
                y = np.array(self.price_ETHUSDT).reshape((len(self.time_ETHUSDT), 1))
                linear = LinearRegression().fit(x, y)
                slope: float = linear.coef_[0][0] / current_price * 100
                if abs(slope) >= 1:
                    print("Цена изменилась на: %.2f%% " % slope)
                    self.time_ETHUSDT.clear()
                    self.price_ETHUSDT.clear()
