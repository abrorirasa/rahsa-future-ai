import asyncio
from exchange.binance_connector import get_klines
from trading_engine.backtest import run_backtest

async def main():
    print("Mengambil data historis...")
    klines = await get_klines("BTCUSDT", interval="4h", limit=500)
    closing_prices = [float(k[4]) for k in klines]

    print(f"Menjalankan backtest terhadap {len(closing_prices)} data...")
    result = run_backtest(closing_prices, initial_capital=1000.0)

    print("\n=== HASIL BACKTEST (BUKAN jaminan masa depan) ===")
    print(f"Total trade: {result['total_trades']}")
    print(f"Winrate: {result['winrate_percent']}%")
    print(f"Modal awal: $1000 -> Modal akhir: ${result['final_capital']}")
    print(f"Return: {result['return_percent']}%")
    print(f"Rata-rata untung per trade: {result['avg_win_percent']}%")
    print(f"Rata-rata rugi per trade: {result['avg_loss_percent']}%")

asyncio.run(main())
