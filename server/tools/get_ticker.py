import ccxt
from ..errors import ExchangeNotSupportedError, InvalidSymbolError, APIError
from ..exchanges import get_exchange
from ..cache import Cache

cache = Cache()

def get_ticker(Symbol: str, Exchange: str) -> dict:

    key = f"{Exchange}:{Symbol}"

    if not Symbol or not Exchange:
        raise ValueError("Both 'Symbol' and 'Exchange' parameters are required.")

    cached_data = cache.get(key)

    if cached_data is not None:
        return cached_data
    
    try:
        exchange = get_exchange(Exchange)

        Symbol = Symbol.upper()
        ticker = exchange.fetch_ticker(Symbol)

        result = {
            "symbol": Symbol,
            "exchange": Exchange,
            "last_price": ticker['last'],
            "high": ticker['high'],
            "low": ticker['low'],
            "volume": ticker['baseVolume'],
            "price_change_percent": ticker['percentage']
        }

        cache.save(key, result, ttl=20)

        return result
    
    except ccxt.BadSymbol as e:
        raise InvalidSymbolError(f"Bad symbol '{Symbol}' for exchange '{Exchange}': {str(e)}")
    except ccxt.InvalidOrder as e:
        raise InvalidSymbolError(f"Invalid symbol '{Symbol}' for exchange '{Exchange}': {str(e)}")
    except ccxt.BaseError as e:
        raise APIError(f"An error occurred while fetching data from exchange '{Exchange}': {str(e)}")
    
    except ccxt.NetworkError as e:
        raise APIError(f"Network error while connecting to exchange '{Exchange}': {str(e)}")
    
    except ccxt.ExchangeError as e:
        raise APIError(f"Exchange error from '{Exchange}': {str(e)}")
    
