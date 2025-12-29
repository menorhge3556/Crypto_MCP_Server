import asyncio
from server.tools.get_ticker import get_ticker
from server.tools.get_ohclv import get_ohclv
from server.tools.stream_ticker import stream_ticker

async def main():

    print("\n--- Testing get_ticker ---")
    ticker = get_ticker("BTC/USDT", "binance")
    print(ticker)

    print("\n--- Testing get_ohclv ---")
    candles = await get_ohclv("BTC/USDT", "binance", "1m", 3)
    print(candles)

    print("\n--- Testing stream_ticker (3 updates) ---")
    async for update in stream_ticker("BTC/USDT", "binance", interval=2):
        print(update)
        break  

asyncio.run(main())
