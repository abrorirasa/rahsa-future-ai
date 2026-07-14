import asyncio
from exchange.binance_connector import get_klines
from trading_engine.rsi_strategy import generate_rsi_signal

SL, TP = 5.0, 10.0

async def backtest(limit):
    klines = await get_klines("BTCUSDT", interval="4h", limit=limit)
    prices = [float(k[4]) for k in klines]
    position = None
    entry_price = 0
    trades = []
    for i in range(20, len(prices)):
        wp = prices[:i+1]
        price_now = prices[i]
        if position == "LONG":
            pnl_now = (price_now - entry_price) / entry_price * 100
            if pnl_now <= -SL or pnl_now >= TP:
                trades.append(pnl_now); position = None; continue
        r = generate_rsi_signal(wp)
        if position is None and r["signal"] == "BUY":
            position = "LONG"; entry_price = price_now
        elif position == "LONG" and r["signal"] == "SELL":
            pnl = (price_now - entry_price) / entry_price * 100
            trades.append(pnl); position = None
    total = round(sum(trades), 2)
    wr = round(len([t for t in trades if t>0])/len(trades)*100, 2) if trades else 0
    return len(trades), wr, total

async def main():
    lines = ["=== VALIDASI BTC+RSI DI BEBERAPA PERIODE ===\n"]
    for limit in [500, 1000, 1500]:
        n, wr, pnl = await backtest(limit)
        hari = limit * 4 // 24
        lines.append(f"{limit} candle (~{hari} hari): {n} trade, winrate {wr}%, PnL {pnl}%")
    output = "\n".join(lines)
    print(output)
    with open("hasil_validasi_btc_rsi.txt", "w") as f:
        f.write(output)

asyncio.run(main())
