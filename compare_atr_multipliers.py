import asyncio
from exchange.binance_connector import get_klines
from trading_engine.combined_strategy import generate_combined_signal

SYMBOLS = ["BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT","ADAUSDT",
           "DOGEUSDT","DOTUSDT","AVAXUSDT","MATICUSDT","LTCUSDT","LINKUSDT"]
CANDLES_PER_PERIOD = 1000
NUM_PERIODS = 6
ATR_PERIOD = 14

# Kombinasi (SL_multiplier, TP_multiplier) yang mau dites
COMBOS = [
    (1.0, 2.0),
    (1.5, 3.0),
    (2.0, 3.0),
    (2.0, 4.0),
    (1.5, 4.5),
]


def calculate_atr(highs, lows, closes, period=14):
    if len(closes) < period + 1:
        return None
    trs = []
    for i in range(-period, 0):
        high = highs[i]
        low = lows[i]
        prev_close = closes[i - 1]
        tr = max(high - low, abs(high - prev_close), abs(low - prev_close))
        trs.append(tr)
    return sum(trs) / period


async def fetch_periods(symbol, interval="4h", candles_per_period=1000, num_periods=3):
    periods = {}
    end_time = None
    for period_idx in range(1, num_periods + 1):
        klines = await get_klines(symbol, interval=interval, limit=candles_per_period, end_time=end_time)
        if not klines:
            break
        periods[period_idx] = klines
        end_time = klines[0][0] - 1
    return periods


def backtest_atr(closes, highs, lows, sl_mult, tp_mult):
    position = None
    entry_price = 0
    sl_price = 0
    tp_price = 0
    trades = []

    for i in range(50, len(closes)):
        wc = closes[:i+1]
        wh = highs[:i+1]
        wl = lows[:i+1]
        price_now = closes[i]

        if position == "LONG":
            if price_now <= sl_price:
                pnl = (price_now - entry_price) / entry_price * 100
                trades.append(pnl); position = None; continue
            elif price_now >= tp_price:
                pnl = (price_now - entry_price) / entry_price * 100
                trades.append(pnl); position = None; continue

        r = generate_combined_signal(wc)
        if r["signal"] == "NOT_ENOUGH_DATA":
            continue

        atr = calculate_atr(wh, wl, wc, ATR_PERIOD)
        if atr is None:
            continue

        if position is None and r["signal"] == "BUY":
            position = "LONG"
            entry_price = price_now
            sl_price = entry_price - (atr * sl_mult)
            tp_price = entry_price + (atr * tp_mult)
        elif position == "LONG" and r["signal"] == "SELL":
            pnl = (price_now - entry_price) / entry_price * 100
            trades.append(pnl); position = None

    total = round(sum(trades), 2) if trades else 0
    wr = round(len([t for t in trades if t > 0]) / len(trades) * 100, 2) if trades else 0
    return len(trades), wr, total


async def main():
    # Fetch data sekali saja per symbol, dipakai ulang buat semua kombinasi multiplier
    all_periods = {}
    for symbol in SYMBOLS:
        all_periods[symbol] = await fetch_periods(symbol, "4h", CANDLES_PER_PERIOD, NUM_PERIODS)
        await asyncio.sleep(0.3)

    lines = ["=== PERBANDINGAN KOMBINASI SL/TP MULTIPLIER ATR ===\n"]
    summary = []

    for sl_mult, tp_mult in COMBOS:
        in_total = 0; in_count = 0; in_trades = 0
        out_total = 0; out_count = 0; out_trades = 0

        for symbol, periods in all_periods.items():
            for p_idx, klines in periods.items():
                closes = [float(k[4]) for k in klines]
                highs = [float(k[2]) for k in klines]
                lows = [float(k[3]) for k in klines]
                n, wr, pnl = backtest_atr(closes, highs, lows, sl_mult, tp_mult)
                if p_idx <= 3:
                    in_total += pnl; in_count += 1; in_trades += n
                else:
                    out_total += pnl; out_count += 1; out_trades += n

        in_avg = round(in_total / in_count, 2) if in_count else 0
        out_avg = round(out_total / out_count, 2) if out_count else 0
        label = f"SL {sl_mult}x ATR / TP {tp_mult}x ATR"
        lines.append(f"{label}: IN-SAMPLE (P1-3) {in_avg:+.2f}% ({in_trades} trade)  |  OUT-OF-SAMPLE (P4-6) {out_avg:+.2f}% ({out_trades} trade)")
        summary.append((label, out_avg, out_trades))

    lines.append("\n=== RANKING BERDASARKAN OUT-OF-SAMPLE (P4-6) ===")
    summary.sort(key=lambda x: x[1], reverse=True)
    for label, avg, n_trades in summary:
        lines.append(f"{label}: {avg:+.2f}% ({n_trades} trade)")

    output = "\n".join(lines)
    print(output)
    with open("hasil_perbandingan_atr_multiplier.txt", "w") as f:
        f.write(output)


asyncio.run(main())
