"""
Optimasi Stop Loss - mencoba beberapa nilai SL/TP untuk mencari yang paling seimbang.
"""
import asyncio
from exchange.binance_connector import get_klines
from trading_engine.strategy import calculate_ma

async def simulate_with_params(prices, stop_loss_pct, take_profit_pct):
    position = None
    entry_price = 0
    trades = []

    for i in range(50, len(prices)):
        window = prices[:i+1]
        ma20_now = calculate_ma(window, 20)
        ma50_now = calculate_ma(window, 50)
        ma20_prev = calculate_ma(window[:-1], 20)
        ma50_prev = calculate_ma(window[:-1], 50)
        price_now = prices[i]

        if position == "LONG":
            pnl_now = (price_now - entry_price) / entry_price * 100
            if pnl_now <= -stop_loss_pct:
                trades.append(pnl_now)
                position = None
                continue
            elif pnl_now >= take_profit_pct:
                trades.append(pnl_now)
                position = None
                continue

        if position is None and ma20_prev <= ma50_prev and ma20_now > ma50_now:
            position = "LONG"
            entry_price = price_now
        elif position == "LONG" and ma20_prev >= ma50_prev and ma20_now < ma50_now:
            pnl = (price_now - entry_price) / entry_price * 100
            trades.append(pnl)
            position = None

    total_pnl = sum(trades)
    wins = [t for t in trades if t > 0]
    winrate = (len(wins) / len(trades) * 100) if trades else 0
    return {
        "sl": stop_loss_pct, "tp": take_profit_pct,
        "total_trades": len(trades), "winrate": round(winrate, 2),
        "total_pnl": round(total_pnl, 2)
    }

async def main():
    klines = await get_klines("SOLUSDT", interval="4h", limit=200)
    prices = [float(k[4]) for k in klines]

    combos = [
        (2.0, 4.0), (3.0, 6.0), (4.0, 8.0), (5.0, 10.0), (2.0, 6.0), (3.0, 9.0),
    ]

    lines = ["=== OPTIMASI STOP LOSS / TAKE PROFIT (SOLUSDT) ===\n"]
    results = []
    for sl, tp in combos:
        r = await simulate_with_params(prices, sl, tp)
        line = f"SL:{sl}% TP:{tp}% -> {r['total_trades']} trade, winrate {r['winrate']}%, total PnL {r['total_pnl']}%"
        lines.append(line)
        results.append(r)

    best = max(results, key=lambda x: x['total_pnl'])
    lines.append(f"\nPALING OPTIMAL: SL:{best['sl']}% TP:{best['tp']}% dengan total PnL {best['total_pnl']}%")

    output = "\n".join(lines)
    print(output)
    with open("hasil_optimasi.txt", "w") as f:
        f.write(output)

asyncio.run(main())
