from server.exchanges import get_exchange
import asyncio
import ccxt
from server.errors import ExchangeNotSupportedError, InvalidSymbolError, APIError

async def stream_ticker(symbol: str, exchange: str, interval: int):

    if symbol is None or exchange is None:
        raise ValueError("Both 'symbol' and 'exchange' parameters are required.")
    
    if interval < 1:
        raise ValueError("Interval must be at least 1 second.")
    
    if symbol.strip() == "" or exchange.strip() == "":
        raise ValueError("Both 'symbol' and 'exchange' parameters cannot be empty.")
    
    exchange_instance = get_exchange(exchange)
    symbol = symbol.upper()
    exchange_instance.load_markets()
    
    if symbol not in exchange_instance.symbols:
        raise InvalidSymbolError(f"Symbol '{symbol}' is not supported on exchange '{exchange}'.")
    
    while True:
        try:
            ticker = exchange_instance.fetch_ticker(symbol)

            data = {
                "symbol": symbol,
                "exchange": exchange,
                "last_price": ticker['last'],
                "high": ticker['high'],
                "low": ticker['low'],
                "volume": ticker['baseVolume'],
                "price_change_percent": ticker['percentage']
            }

            yield data

        except asyncio.CancelledError:
            break

        except:
            yield {"error": f"Failed to fetch ticker for {symbol} on {exchange}."}

        await asyncio.sleep(interval)   
