from ccxt import binance


async def get_data(exchange: binance):
    return exchange.fetch_ticker('ETH/USDT')['last']
