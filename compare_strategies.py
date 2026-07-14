import asyncio
from exchange.binance_connector import get_klines
from trading_engine.strategy import generate_signal
from ai_engine.decision_engine import make_decision

async def backtest(symbol, use_ai, limit=1000):
    klines = await get_klines(symbol, interval="4h", limit=limit)
    prices = [float(k[4]) for k in klines]
    volumes = [float(k[5]) for k in klines]
    position = None
    entry_price = 0
    trades = []
    SL, TP = 5.0, 10.0

    for i in range(50, len(prices)):
        wp, wv = prices[:i+1], volumes[:i+1]
        price_now = prices[i]
        if position == "LONG":
            pnl_now = (price_now - entry_price) / entry_price * 100
            if pnl_now <= -SL or pnl_now >= TP:
                trades.append(pnl_now); position = None; continue

        if use_ai:
            d = make_decision(wp, wv)
            action = d["action"]
        else:
            s = generate_signal(wp)
            action = s["signal"]

        if position is None and action in ("BUY", "STRONG_BUY"):
            position = "LONG"; entry_price = price_now
        elif position == "LONG" and action in ("SELL", "STRONG_SELL"):
            pnl = (price_now - entry_price) / entry_price * 100
            trades.append(pnl); position = None

    total = round(sum(trades), 2)
    wr = round(len([t for t in trades if t>0])/len(trades)*100, 2) if trades else 0
    return len(trades), wr, total

async def main():
    lines = ["=== MA MURNI vs DECISION ENGINE (1000 candle) ===\n"]
    for symbol in ["BTCUSDT", "MATICUSDT", "ADAUSDT"]:
        n1, wr1, pnl1 = await backtest(symbol, use_ai=False)
        n2, wr2, pnl2 = await backtest(symbol, use_ai=True)
        lines.append(f"{symbol} MA-murni: {n1} trade, {wr1}% winrate, PnL {pnl1}%")
        lines.append(f"{symbol} +AI:      {n2} trade, {wr2}% winrate, PnL {pnl2}%\n")
    output = "\n".join(lines)
    print(output)
    with open("hasil_perbandingan.txt", "w") as f:
        f.write(output)

asyncio.run(main())
