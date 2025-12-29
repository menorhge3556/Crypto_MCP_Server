# 🚀 Crypto MCP Server
## 📌 Overview

Crypto MCP Server is a Model Context Protocol (MCP) compatible server that provides real-time and historical cryptocurrency market data using ccxt.
It exposes three fully tested tools:

get_ticker → Live price & market summary

get_ohclv → Historical candlestick data

stream_ticker → Real-time price streaming (async generator)

The project includes:

Custom error handling

In-memory caching

A lightweight MCP server architecture

Complete test suite (pytest)

Local client for manual testing

## ✨ Features
🔹 get_ticker

Fetches:

last price

high & low

base volume

price_change_percent

🔹 get_ohclv

Fetches OHLCV candles with:

timestamp

open

high

low

close

volume

🔹 stream_ticker

Real-time streaming ticker with async generator that yields updates every N seconds.

## 🧩 Project Structure
crypto-mcp-server/
│
├── server/
│   ├── main.py
│   ├── mcp_server.py
│   ├── cache.py
│   ├── errors.py
│   ├── exchanges.py
│   └── tools/
│       ├── get_ticker.py
│       ├── get_ohclv.py
│       └── stream_ticker.py
│
├── tests/
│   ├── test_get_ticker.py
│   ├── test_ohclv.py
│   └── test_stream_ticker.py
│
├── client_test.py
├── README.md
├── requirements.txt
└── .gitignore

## 🛠️ Tech Stack

Python 3.10+

ccxt for exchange APIs

pytest for testing

asyncio for streaming

MCP server protocol style

## 📦 Installation
git clone https://github.com/yourusername/crypto-mcp-server
cd crypto-mcp-server
pip install -r requirements.txt

## ▶️ Running the MCP Server

From the server/ directory:

python -m server.main


You should see:

Crypto MCP Server running…
Registered tools: get_ticker, get_ohclv, stream_ticker

## 🧪 Running Tests

All tests are under tests/ and cover:

Valid/invalid symbols

Unsupported exchanges

API errors

Streaming behavior

Run:

pytest -vv

## 📁 Tools Implemented
### 🔹 get_ticker

Handles:

Invalid symbols

Unsupported exchanges

ccxt API exceptions

Caching responses for 20 seconds

### 🔹 get_ohclv

Returns OHCLV historical candles

Validates timeframe & limit

Raises custom errors

### 🔹 stream_ticker

Async generator

Streams live ticker updates

Internal delay using asyncio.sleep()

Full validation & error handling

### Caching Layer

cache.py implements simple in-memory TTL cache:

save(key, value, ttl)

get(key)

Prevents extra API calls

## 🧪 Testing Strategy
### Unit Tests (pytest)

Each tool has:

success test

invalid symbol test

invalid exchange test

API failure test

### Streaming Tests

Uses asyncio.mark

Simulates multiple ticker updates

Checks generator behavior

## 🧪 Local Testing Without MCP CLI

Run:

python client_test.py


It prints:

get_ticker result

get_ohclv candles

3 streamed ticker updates

## 🔍 Example Output
--- Testing get_ticker ---
{...}

--- Testing get_ohclv ---
{...}

--- Testing stream_ticker ---
{...}

## 📌 Key Learning & Highlights

Designed full MCP-style server

Implemented async streaming tool

Wrote complete test suite

Built caching + error handling abstraction

Validated exchange + symbol inputs safely
