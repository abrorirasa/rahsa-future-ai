import asyncio
from exchange.binance_connector import get_klines
from trading_engine.strategy import generate_signal

async def main():
    klines = await get_klines("BTCUSDT", interval="1h", limit=60)
    closing_prices = [float(k[4]) for k in klines]
    result = generate_signal(closing_prices)
    print("BERHASIL analisa strategi MA20/MA50!")
    print(f"Sinyal saat ini: {result['signal']}")
    print(f"MA20: {result['ma20']}, MA50: {result['ma50']}")

asyncio.run(main())
