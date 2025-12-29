import pytest
import asyncio
from server.tools.stream_ticker import stream_ticker
from server.errors import InvalidSymbolError, ExchangeNotSupportedError

@pytest.mark.asyncio
async def async_enumerate(aiterable):
    index = 0
    async for item in aiterable:
        yield index, item
        index += 1

@pytest.mark.asyncio
async def test_stream_ticker_valid():
    symbol = "BTC/USDT"
    exchange = "binance"
    interval = 1

    stream = stream_ticker(symbol, exchange, interval)

    result = []
    async for idx, data in async_enumerate(stream):
        result.append(data)
        if idx >= 2:  # Collect 3 data points
            break

    for item in result:
        assert "symbol" in item
        assert "exchange" in item
        assert "last_price" in item
        assert "high" in item
        assert "low" in item
        assert "volume" in item
        assert "price_change_percent" in item

@pytest.mark.asyncio
async def test_stream_ticker_invalid_symbol():
    symbol = "INVALID/SYMBOL"
    exchange = "binance"
    interval = 1

    with pytest.raises(InvalidSymbolError):
        stream = stream_ticker(symbol, exchange, interval)
        await stream.__anext__()

@pytest.mark.asyncio
async def test_stream_ticker_invalid_exchange():
    symbol = "BTC/USDT"
    exchange = "invalid_exchange"
    interval = 1

    with pytest.raises(ExchangeNotSupportedError):
        stream = stream_ticker(symbol, exchange, interval)
        await stream.__anext__()

@pytest.mark.asyncio
async def test_stream_ticker_invalid_interval():
    symbol = "BTC/USDT"
    exchange = "binance"
    interval = 0  # Invalid interval

    with pytest.raises(ValueError):
        stream = stream_ticker(symbol, exchange, interval)
        await stream.__anext__()