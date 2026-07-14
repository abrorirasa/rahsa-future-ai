"""
Simulasi Paper Trading V2 - dengan Stop Loss per posisi
Sistem sekarang keluar otomatis jika rugi menyentuh batas stop-loss,
tidak menunggu sinyal SELL dari MA crossover.
"""
import asyncio
from exchange.binance_connector import get_klines
from trading_engine.strategy import calculate_ma
from trading_engine.risk_management import RiskManager

STOP_LOSS_PERCENT = 3.0  # keluar otomatis jika rugi 3%
TAKE_PROFIT_PERCENT = 6.0  # ambil untung otomatis jika untung 6%

async def simulate(symbol="SOLUSDT", capital=1000.0):
    klines = await get_klines(symbol, interval="4h", limit=200)
    prices = [float(k[4]) for k in klines]

    rm = RiskManager(capital=capital)
    position = None
    entry_price = 0
    log = []

    for i in range(50, len(prices)):
        window = prices[:i+1]
        ma20_now = calculate_ma(window, 20)
        ma50_now = calculate_ma(window, 50)
        ma20_prev = calculate_ma(window[:-1], 20)
        ma50_prev = calculate_ma(window[:-1], 50)
        price_now = prices[i]

        if position == "LONG":
            pnl_now = (price_now - entry_price) / entry_price * 100
            if pnl_now <= -STOP_LOSS_PERCENT:
                rm.register_trade_result(pnl_now)
                log.append(f"STOP LOSS kena di harga {price_now}, PnL: {round(pnl_now,2)}%")
                position = None
                continue
            elif pnl_now >= TAKE_PROFIT_PERCENT:
                rm.register_trade_result(pnl_now)
                log.append(f"TAKE PROFIT kena di harga {price_now}, PnL: {round(pnl_now,2)}%")
                position = None
                continue

        if position is None and ma20_prev <= ma50_prev and ma20_now > ma50_now:
            check = rm.can_open_position()
            if check["allowed"]:
                position = "LONG"
                entry_price = price_now
                rm.open_position()
                log.append(f"BUY di harga {price_now} (SL: {round(entry_price*(1-STOP_LOSS_PERCENT/100),2)}, TP: {round(entry_price*(1+TAKE_PROFIT_PERCENT/100),2)})")
            else:
                log.append(f"Sinyal BUY muncul tapi DITOLAK: {check['reason']}")

        elif position == "LONG" and ma20_prev >= ma50_prev and ma20_now < ma50_now:
            pnl = (price_now - entry_price) / entry_price * 100
            rm.register_trade_result(pnl)
            log.append(f"SELL (sinyal MA) di harga {price_now}, PnL: {round(pnl,2)}%")
            position = None

    output = "\n".join(log)
    output += f"\n\nTotal PnL harian terakhir: {round(rm.daily_pnl_percent,2)}%"
    output += f"\nTrading dihentikan otomatis? {rm.trading_halted}"
    print(output)
    with open("hasil_simulasi_v2.txt", "w") as f:
        f.write(output)

asyncio.run(simulate())
