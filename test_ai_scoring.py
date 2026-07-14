import asyncio
from exchange.binance_connector import get_klines
from trading_engine.strategy import generate_signal
from ai_engine.scoring import calculate_final_score

async def main():
    klines = await get_klines("SOLUSDT", interval="4h", limit=60)
    prices = [float(k[4]) for k in klines]
    volumes = [float(k[5]) for k in klines]

    ma_result = generate_signal(prices)
    ai_result = calculate_final_score(prices, volumes, ma_result["signal"])

    output = f"""=== AI SCORING ENGINE - SOLUSDT ===
Sinyal MA20/MA50: {ma_result['signal']}
Keputusan AI: {ai_result['decision']}
Skor akhir: {ai_result['final_score']}

Rincian skor:
- Trend: {ai_result['breakdown']['trend_score']}
- Volume: {ai_result['breakdown']['volume_score']}
- Momentum: {ai_result['breakdown']['momentum_score']}
- Bonus sinyal MA: {ai_result['breakdown']['ma_signal_bonus']}
"""
    print(output)
    with open("hasil_ai_scoring.txt", "w") as f:
        f.write(output)

asyncio.run(main())
