from .mcp_server import CryptoMCPServer
from .tools.get_ticker import get_ticker
from .tools.stream_ticker import stream_ticker
from .tools.get_ohclv import get_ohclv
import asyncio

async def main():
    server = CryptoMCPServer()

    # Register the get_ticker tool
    server.register_tool(
        name="get_ticker",
        handler=get_ticker,
        input_schema= {
            "type": "object",
            "properties": {
                "Symbol": {
                    "type": "string", "description": "The trading pair symbol, e.g., 'BTC/USDT'."
                    },
                "Exchange": {
                    "type": "string", "description": "The exchange name, e.g., 'binance'."
                    }
            },
            "required": [
                "Symbol", "Exchange"
                ]
        },
        output_schema= {
            "type": "object",
            "properties": {
                "symbol": {"type": "string"},
                "exchange": {"type": "string"},
                "last_price": {"type": "number"},
                "high": {"type": "number"},
                "low": {"type": "number"},
                "volume": {"type": "number"},
                "price_change_percent": {"type": "number"}
            },
            "required": [
                "symbol", 
                "exchange", 
                "last_price", 
                "high", 
                "low", 
                "volume", 
                "price_change_percent"
                ]
        },
        streaming=False
    )

    # Register the streaming tool
    server.register_tool(
        name="stream_ticker",
        handler=stream_ticker,
        input_schema= {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string", "description": "The trading pair symbol, e.g., 'BTC/USDT'."
                    },
                "exchange": {
                    "type": "string", "description": "The exchange name, e.g., 'binance'."
                    },
                "interval": {
                    "type": "integer", "description": "The interval in seconds between data fetches."
                    }
            },
            "required": [
                "symbol", 
                "exchange", 
                "interval"
                ]
        },
        output_schema= {
            "type": "object",
            "properties": {
                "symbol": {"type": "string"},
                "exchange": {"type": "string"},
                "last_price": {"type": "number"},
                "high": {"type": "number"},
                "low": {"type": "number"},
                "volume": {"type": "number"},
                "price_change_percent": {"type": "number"}
            },
            "required": [
                "symbol", 
                "exchange", 
                "last_price", 
                "high", 
                "low", 
                "volume", 
                "price_change_percent"
                ],
        },
        streaming=True
    )   

    # Register the get_ohlcv tool
    server.register_tool(
        name="get_ohlcv",
        handler=get_ohclv,
        input_schema={
            "type": "object",
            "properties": {
                "Symbol": {
                    "type": "string",
                    "description": "Market pair, e.g., 'BTC/USDT'."
                },
                "Exchange": {
                    "type": "string",
                    "description": "Exchange name, e.g., 'binance'."
                },
                "Timeframe": {
                    "type": "string",
                    "description": "Timeframe like 1m, 5m, 1h, 1d."
                },
                "Limit": {
                    "type": "integer",
                    "description": "Number of candles to fetch."
                }
            },
            "required": ["Symbol", "Exchange", "Timeframe", "Limit"],
        },
        output_schema={
            "type": "object",
            "properties": {
                "symbol": {"type": "string"},
                "exchange": {"type": "string"},
                "timeframe": {"type": "string"},
                "limit": {"type": "integer"},
                "candles": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "timestamp": {"type": "number"},
                            "open": {"type": "number"},
                            "high": {"type": "number"},
                            "low": {"type": "number"},
                            "close": {"type": "number"},
                            "volume": {"type": "number"}
                        }
                    }
                }
            },
            "required": ["symbol", "exchange", "timeframe", "limit", "candles"]
        }
    )

    await server.run()

if __name__ == "__main__":
    asyncio.run(main())

