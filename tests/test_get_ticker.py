import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from server.tools.get_ticker import get_ticker
from server.errors import APIError, InvalidSymbolError, ExchangeNotSupportedError as Exc

def test_get_ticker_valid():
    #Eample: Binance BTC/USDT
    symbol = "BTC/USDT"
    exchange = "binance"
    result = get_ticker(symbol, exchange)

    assert result["symbol"] == symbol
    assert result["exchange"] == exchange
    assert "last_price" in result
    assert "high" in result
    assert "low" in result
    assert "volume" in result
    assert "price_change_percent" in result

def test_get_ticker_invalid_symbol():
    symbol = "INVALID/SYMBOL"
    exchange = "binance"
    
    with pytest.raises(InvalidSymbolError):
        get_ticker(symbol, exchange)

def test_get_ticker_invalid_exchange():
    symbol = "BTC/USDT"
    exchange = "invalid_exchange"
    
    with pytest.raises(Exc):
        get_ticker(symbol, exchange)

def test_get_ticker_api_error():
    exchange = "binance"
    symbol = None
    
    with pytest.raises(ValueError):
        get_ticker(symbol, exchange)
