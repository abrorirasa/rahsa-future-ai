import asyncio
from exchange.binance_connector import get_klines
from trading_engine.combined_strategy import generate_combined_signal

SL, TP = 5.0, 10.0
SYMBOLS = ["BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT","ADAUSDT","DOGEUSDT","DOTUSDT","AVAXUSDT","MATICUSDT","LTCUSDT","LINKUSDT"]

async def backtest(symbol, limit=1000):
    klines = await get_klines(symbol, interval="4h", limit=limit)
    prices = [float(k[4]) for k in klines]
    position = None
    entry_price = 0
    trades = []
    for i in range(50, len(prices)):
        wp = prices[:i+1]
        price_now = prices[i]
        if position == "LONG":
            pnl_now = (price_now - entry_price) / entry_price * 100
            if pnl_now <= -SL or pnl_now >= TP:
                trades.append(pnl_now); position = None; continue
        r = generate_combined_signal(wp)
        if position is None and r["signal"] == "BUY":
            position = "LONG"; entry_price = price_now
        elif position == "LONG" and r["signal"] == "SELL":
            pnl = (price_now - entry_price) / entry_price * 100
            trades.append(pnl); position = None
    total = round(sum(trades), 2)
    wr = round(len([t for t in trades if t>0])/len(trades)*100, 2) if trades else 0
    return len(trades), wr, total

async def main():
    lines = ["=== STRATEGI GABUNGAN MA+RSI (1000 candle) ===\n"]
    total_pnl_all = 0
    for symbol in SYMBOLS:
        n, wr, pnl = await backtest(symbol)
        lines.append(f"{symbol}: {n} trade, winrate {wr}%, PnL {pnl}%")
        total_pnl_all += pnl
        await asyncio.sleep(0.3)
    lines.append(f"\nRata-rata PnL semua koin: {round(total_pnl_all/len(SYMBOLS), 2)}%")
    output = "\n".join(lines)
    print(output)
    with open("hasil_combined.txt", "w") as f:
        f.write(output)

asyncio.run(main())
