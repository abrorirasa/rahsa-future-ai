"""
Konektor Binance - Phase 2: Market Data Engine
Tahap ini HANYA membaca data publik (harga pasar), TIDAK ada API key,
TIDAK ada eksekusi order. Aman sepenuhnya untuk dites.
"""
import httpx

BINANCE_BASE_URL = "https://api.binance.com"

async def get_price(symbol: str = "BTCUSDT") -> dict:
    """Ambil harga terkini untuk satu simbol, misal BTCUSDT."""
    url = f"{BINANCE_BASE_URL}/api/v3/ticker/price"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params={"symbol": symbol})
        response.raise_for_status()
        return response.json()

async def get_klines(symbol: str = "BTCUSDT", interval: str = "1h", limit: int = 5) -> list:
    """Ambil data candlestick (buat nanti dipakai strategi MA20/MA50)."""
    url = f"{BINANCE_BASE_URL}/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        return response.json()
