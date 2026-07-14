"""
Simulasi Paper Trading - menggabungkan Strategy + Risk Management
Tanpa uang asli, murni simulasi untuk melihat sistem bekerja bersama.
"""
import asyncio
from exchange.binance_connector import get_klines
from trading_engine.strategy import calculate_ma
from trading_engine.risk_management import RiskManager

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

        if position is None and ma20_prev <= ma50_prev and ma20_now > ma50_now:
            check = rm.can_open_position()
            if check["allowed"]:
                position = "LONG"
                entry_price = price_now
                rm.open_position()
                log.append(f"BUY di harga {price_now}")
            else:
                log.append(f"Sinyal BUY muncul tapi DITOLAK: {check['reason']}")

        elif position == "LONG" and ma20_prev >= ma50_prev and ma20_now < ma50_now:
            pnl = (price_now - entry_price) / entry_price * 100
            rm.register_trade_result(pnl)
            log.append(f"SELL di harga {price_now}, PnL: {round(pnl,2)}%")
            position = None

    output = "\n".join(log)
    output += f"\n\nTotal PnL harian terakhir: {rm.daily_pnl_percent}%"
    output += f"\nTrading dihentikan otomatis? {rm.trading_halted}"
    print(output)
    with open("hasil_simulasi.txt", "w") as f:
        f.write(output)

asyncio.run(simulate())
