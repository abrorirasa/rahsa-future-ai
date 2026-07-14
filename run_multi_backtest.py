import asyncio
from exchange.binance_connector import get_klines
from trading_engine.backtest import run_backtest

SYMBOLS = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT",
    "XRPUSDT", "ADAUSDT", "DOGEUSDT", "DOTUSDT",
    "AVAXUSDT", "MATICUSDT", "LTCUSDT", "LINKUSDT",
]

async def analyze_symbol(symbol):
    try:
        klines = await get_klines(symbol, interval="4h", limit=500)
        closing_prices = [float(k[4]) for k in klines]
        result = run_backtest(closing_prices, initial_capital=1000.0)
        return symbol, result
    except Exception as e:
        return symbol, {"error": str(e)}

async def main():
    lines = []
    lines.append("=== HASIL BACKTEST 12 ASET ===\n")
    summary = []
    for symbol in SYMBOLS:
        sym, result = await analyze_symbol(symbol)
        if "error" in result:
            lines.append(f"{sym}: GAGAL - {result['error']}")
            continue
        line = f"{sym}: {result['total_trades']} trade, winrate {result['winrate_percent']}%, return {result['return_percent']}%"
        lines.append(line)
        summary.append((sym, result))
        await asyncio.sleep(0.3)

    lines.append("\n=== RANKING BERDASARKAN RETURN ===")
    ranked = sorted(summary, key=lambda x: x[1]['return_percent'], reverse=True)
    for sym, result in ranked:
        lines.append(f"{sym}: return {result['return_percent']}% (winrate {result['winrate_percent']}%, {result['total_trades']} trade)")

    output = "\n".join(lines)
    print(output)
    with open("hasil_backtest.txt", "w") as f:
        f.write(output)
    print("\n\nHasil juga disimpan di file hasil_backtest.txt")

asyncio.run(main())
