import ccxt
from server.errors import ExchangeNotSupportedError, InvalidSymbolError, APIError
from server.exchanges import get_exchange
from server.cache import Cache

cache = Cache()

async def get_ohclv(Symbol: str, Exchange: str, Timeframe: str, Limit: int) -> dict:

    cache_key = f"{Exchange}:{Symbol}:{Timeframe}:{Limit}"
    cached_data = cache.get(cache_key)

    if cached_data is not None:
        return cached_data
    
    
    if not Symbol or not Exchange or not Timeframe or Limit is None:
        raise ValueError("Parameters 'Symbol', 'Exchange', 'Timeframe', and 'Limit' are required.")
    
    Symbol = Symbol.upper()
    exchange = get_exchange(Exchange)
    exchange.load_markets()

    if Symbol not in exchange.symbols:
        raise InvalidSymbolError(f"Symbol '{Symbol}' is not supported on exchange '{Exchange}'.")
    
    if Limit <= 0:
        raise ValueError("'Limit' must be a positive integer.")
    
    if Timeframe not in exchange.timeframes:
        raise ValueError(f"Timeframe '{Timeframe}' is not supported on exchange '{Exchange}'.")
    
    try:
        ohclv = exchange.fetch_ohlcv(Symbol, timeframe=Timeframe, limit=Limit)
        result = []

        for entry in ohclv:
            result.append({
                "timestamp": entry[0],
                "open": entry[1],
                "high": entry[2],
                "low": entry[3],
                "close": entry[4],
                "volume": entry[5]
            })

        response = {   
            "symbol": Symbol,
            "exchange": Exchange,
            "timeframe": Timeframe,
            "limit": Limit,
            "candles": result
        }

        cache.save(cache_key, response, ttl=60)

        return response
    
    except ccxt.BaseError as e:
        raise APIError(f"An error occurred while fetching OHCLV data from exchange '{Exchange}': {str(e)}")
    
    except ccxt.NetworkError as e:
        raise APIError(f"Network error while connecting to exchange '{Exchange}': {str(e)}")
    
    except ccxt.ExchangeError as e:
        raise APIError(f"Exchange error from '{Exchange}': {str(e)}")
    
    except ccxt.BadSymbol as e:
        raise InvalidSymbolError(f"Bad symbol '{Symbol}' for exchange '{Exchange}': {str(e)}")
    
    except Exception as e:
        raise APIError(f"An unexpected error occurred: {str(e)}")
    