import asyncio
from exchange.binance_connector import get_klines
from trading_engine.combined_strategy import generate_combined_signal

SYMBOLS = ["BTCUSDT","ETHUSDT","BNBUSDT","SOLUSDT","XRPUSDT","ADAUSDT",
           "DOGEUSDT","DOTUSDT","AVAXUSDT","MATICUSDT","LTCUSDT","LINKUSDT"]
CANDLES_PER_PERIOD = 1000
NUM_PERIODS = 3
ATR_PERIOD = 14
SL_ATR_MULT = 1.5
TP_ATR_MULT = 3.0


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


def backtest_atr(closes, highs, lows):
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
            sl_price = entry_price - (atr * SL_ATR_MULT)
            tp_price = entry_price + (atr * TP_ATR_MULT)
        elif position == "LONG" and r["signal"] == "SELL":
            pnl = (price_now - entry_price) / entry_price * 100
            trades.append(pnl); position = None

    total = round(sum(trades), 2) if trades else 0
    wr = round(len([t for t in trades if t > 0]) / len(trades) * 100, 2) if trades else 0

    cumulative = 0
    peak = 0
    max_dd = 0
    for t in trades:
        cumulative += t
        if cumulative > peak:
            peak = cumulative
        dd = peak - cumulative
        if dd > max_dd:
            max_dd = dd
    max_dd = round(max_dd, 2)

    return len(trades), wr, total, max_dd


async def main():
    lines = ["=== VALIDASI 3-PERIODE: MA+RSI + ATR SL/TP ===\n"]
    grand_total = 0
    grand_count = 0

    for symbol in SYMBOLS:
        periods = await fetch_periods(symbol, "4h", CANDLES_PER_PERIOD, NUM_PERIODS)
        lines.append(f"\n{symbol}:")
        for p_idx, klines in periods.items():
            closes = [float(k[4]) for k in klines]
            highs = [float(k[2]) for k in klines]
            lows = [float(k[3]) for k in klines]
            n, wr, pnl, mdd = backtest_atr(closes, highs, lows)
            lines.append(f"  Period {p_idx}: {n} trade, WR {wr}%, PnL {pnl:+.2f}%, Max Drawdown {mdd:.2f}%")
            grand_total += pnl
            grand_count += 1
        await asyncio.sleep(0.3)

    avg = round(grand_total / grand_count, 2) if grand_count else 0
    lines.append(f"\nRata-rata PnL semua koin & semua periode: {avg:+.2f}%")

    output = "\n".join(lines)
    print(output)
    with open("hasil_validasi_atr_3period.txt", "w") as f:
        f.write(output)


asyncio.run(main())
