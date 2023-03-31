import asyncio
from time import sleep, time
from data import get_data
import threading
import ccxt
import numpy as np
from sklearn.linear_model import LinearRegression


class Detection(threading.Thread):

    def __init__(self):
        super().__init__()
        self.TIME_FOR_WAIT: int = 3600
        self.daemon = True
        self.exchange = ccxt.binance()
        self.time_ETHUSDT: list = []
        self.price_ETHUSDT: list = []
        self.current_time = time()

    async def run(self):

        while True:
            data = await get_data(self.exchange)
            if len(self.time_ETHUSDT) > 0 and self.current_time - self.price_ETHUSDT[0] > self.TIME_FOR_WAIT:
                self.time_ETHUSDT.pop(0)
                self.price_ETHUSDT.pop(0)
            self.time_ETHUSDT.append(self.current_time)
            self.price_ETHUSDT.append(data)
            if len(self.time_ETHUSDT) >= 2:
                x = np.array(self.time_ETHUSDT).reshape((len(self.time_ETHUSDT), 1))
                y = np.array(self.time_ETHUSDT).reshape((len(self.time_ETHUSDT), 1))
                linear = LinearRegression().fit(x, y)
                slope = linear .coef_[0][0] / data * 100
                if abs(slope) >= 1:
                    print("Цена изменилась: %.2f%% " % slope)