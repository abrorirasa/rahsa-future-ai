import asyncio
from exchange.binance_connector import get_price

async def main():
    data = await get_price("BTCUSDT")
    print("BERHASIL ambil harga dari Binance!")
    print(data)

asyncio.run(main())
