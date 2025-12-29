import pytest
from server.tools.get_ohclv import get_ohclv
from server.errors import InvalidSymbolError, APIError, ExchangeNotSupportedError

@pytest.mark.asyncio
async def test_get_ohclv_valid():
    result = await get_ohclv("BTC/USDT", "binance", "1m", 5)

    assert "symbol" in result
    assert "exchange" in result
    assert "timeframe" in result
    assert "limit" in result
    assert "candles" in result
    assert len(result["candles"]) == 5

@pytest.mark.asyncio
async def test_get_ohclv_invalid_symbol():

    with pytest.raises(InvalidSymbolError):
        await get_ohclv("INVALID/SYMBOL", "binance", "1m", 5) 

@pytest.mark.asyncio
async def test_get_ohclv_invalid_exchange():

    with pytest.raises(ExchangeNotSupportedError):
        await get_ohclv("BTC/USDT", "invalid_exchange", "1m", 5)

@pytest.mark.asyncio
async def test_get_ohclv_invalid_timeframe():
    with pytest.raises(ValueError):
        await get_ohclv("BTC/USDT", "binance", "invalid_timeframe", 5)

@pytest.mark.asyncio
async def test_get_ohclv_invalid_limit():
    with pytest.raises(ValueError):
        await get_ohclv("BTC/USDT", "binance", "1m", -1)

@pytest.mark.asyncio
async def test_get_ohclv_missing_parameters():
    with pytest.raises(TypeError):
        await get_ohclv("BTC/USDT", "binance", "1m")  # Missing limit parameter


