from ccxt import binance


async def get_current_value_price(exchange: binance):
    return exchange.fetch_ticker('ETH/USDT')['last']

