"""
Simulasi Paper Trading V3
Upgrade dari v2:
- Strategi: MA+RSI gabungan (combined_strategy), bukan MA solo
- SL/TP dinamis berbasis ATR (Average True Range), bukan persen tetap
- Multi-symbol dalam satu run
- Tetap pertahankan pola v2: stop-loss/take-profit dieksekusi instan,
  tidak menunggu sinyal SELL dari strategi
"""
import asyncio
from exchange.binance_connector import get_klines
from trading_engine.combined_strategy import generate_combined_signal
from trading_engine.risk_management import RiskManager

SYMBOLS = ["BTCUSDT", "SOLUSDT", "LINKUSDT", "LTCUSDT"]
CANDLES = 500
ATR_PERIOD = 14
SL_ATR_MULT = 1.5   # SL = 1.5x ATR (terbukti lebih robust out-of-sample: +0.47% vs 2.0x hanya +0.15%)
TP_ATR_MULT = 3.0   # TP = 3x ATR di atas entry (risk:reward 1:2)


def calculate_atr(highs, lows, closes, period=14):
    """Hitung ATR (Average True Range) dari N candle terakhir."""
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


async def simulate(symbol, capital=1000.0):
    klines = await get_klines(symbol, interval="4h", limit=CANDLES)
    closes = [float(k[4]) for k in klines]
    highs = [float(k[2]) for k in klines]
    lows = [float(k[3]) for k in klines]

    rm = RiskManager(capital=capital)
    position = None
    entry_price = 0
    sl_price = 0
    tp_price = 0
    log = []

    for i in range(50, len(closes)):
        window_close = closes[:i+1]
        window_high = highs[:i+1]
        window_low = lows[:i+1]
        price_now = closes[i]

        if position == "LONG":
            if price_now <= sl_price:
                pnl_now = (price_now - entry_price) / entry_price * 100
                rm.register_trade_result(pnl_now)
                log.append(f"{symbol}: STOP LOSS kena di harga {price_now:.4f}, PnL: {round(pnl_now,2)}%")
                position = None
                continue
            elif price_now >= tp_price:
                pnl_now = (price_now - entry_price) / entry_price * 100
                rm.register_trade_result(pnl_now)
                log.append(f"{symbol}: TAKE PROFIT kena di harga {price_now:.4f}, PnL: {round(pnl_now,2)}%")
                position = None
                continue

        r = generate_combined_signal(window_close)
        if r["signal"] == "NOT_ENOUGH_DATA":
            continue

        atr = calculate_atr(window_high, window_low, window_close, ATR_PERIOD)
        if atr is None:
            continue

        if position is None and r["signal"] == "BUY":
            check = rm.can_open_position()
            if check["allowed"]:
                position = "LONG"
                entry_price = price_now
                sl_price = entry_price - (atr * SL_ATR_MULT)
                tp_price = entry_price + (atr * TP_ATR_MULT)
                rm.open_position()
                log.append(
                    f"{symbol}: BUY di harga {price_now:.4f} "
                    f"(ATR: {round(atr,4)}, SL: {round(sl_price,4)}, TP: {round(tp_price,4)})"
                )
            else:
                log.append(f"{symbol}: Sinyal BUY muncul tapi DITOLAK: {check['reason']}")

        elif position == "LONG" and r["signal"] == "SELL":
            pnl = (price_now - entry_price) / entry_price * 100
            rm.register_trade_result(pnl)
            log.append(f"{symbol}: SELL (sinyal strategi) di harga {price_now:.4f}, PnL: {round(pnl,2)}%")
            position = None

    return log, rm


async def main():
    all_log = ["=== SIMULASI PAPER TRADING V3: MA+RSI + ATR SL/TP ===\n"]
    for symbol in SYMBOLS:
        log, rm = await simulate(symbol)
        all_log.append(f"\n--- {symbol} ---")
        all_log.extend(log)
        all_log.append(f"Total PnL harian terakhir: {round(rm.daily_pnl_percent, 2)}%")
        all_log.append(f"Trading dihentikan otomatis?: {rm.trading_halted}")
        await asyncio.sleep(0.3)

    output = "\n".join(all_log)
    print(output)
    with open("hasil_simulasi_v3.txt", "w") as f:
        f.write(output)


asyncio.run(main())
