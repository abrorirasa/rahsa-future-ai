import asyncio
from exchange.binance_connector import get_klines
from ai_engine.decision_engine import make_decision
from trading_engine.risk_management import RiskManager

SYMBOLS = ["BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT","ADAUSDT","DOGEUSDT","DOTUSDT","AVAXUSDT","MATICUSDT","LTCUSDT","LINKUSDT"]
STOP_LOSS = 5.0
TAKE_PROFIT = 10.0

async def backtest_symbol(symbol):
    klines = await get_klines(symbol, interval="4h", limit=200)
    prices = [float(k[4]) for k in klines]
    volumes = [float(k[5]) for k in klines]
    rm = RiskManager(capital=1000.0, max_daily_loss_percent=100.0)
    position = None
    entry_price = 0
    trades = []

    for i in range(50, len(prices)):
        window_p = prices[:i+1]
        window_v = volumes[:i+1]
        price_now = prices[i]

        if position == "LONG":
            pnl_now = (price_now - entry_price) / entry_price * 100
            if pnl_now <= -STOP_LOSS or pnl_now >= TAKE_PROFIT:
                trades.append(pnl_now)
                position = None
                continue

        decision = make_decision(window_p, window_v)
        if position is None and decision["action"] in ("BUY", "STRONG_BUY"):
            position = "LONG"
            entry_price = price_now
        elif position == "LONG" and decision["action"] in ("SELL", "STRONG_SELL"):
            pnl = (price_now - entry_price) / entry_price * 100
            trades.append(pnl)
            position = None

    total_pnl = round(sum(trades), 2)
    wins = [t for t in trades if t > 0]
    winrate = round((len(wins)/len(trades)*100), 2) if trades else 0
    return symbol, len(trades), winrate, total_pnl

async def main():
    lines = ["=== FINAL BACKTEST: Decision Engine (Strategy+AI+Risk) ===\n"]
    for symbol in SYMBOLS:
        sym, n, wr, pnl = await backtest_symbol(symbol)
        lines.append(f"{sym}: {n} trade, winrate {wr}%, total PnL {pnl}%")
        await asyncio.sleep(0.3)
    output = "\n".join(lines)
    print(output)
    with open("hasil_final_backtest.txt", "w") as f:
        f.write(output)

asyncio.run(main())
