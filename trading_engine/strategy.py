"""
Strategi Trading V1: MA20/MA50 Crossover
Sesuai Implementation Decision Notes.

Logika:
- BUY signal: MA20 crossing ABOVE MA50 (trend mulai naik)
- SELL signal: MA20 crossing BELOW MA50 (trend mulai turun)
- Ini strategi sinyal saja, BELUM eksekusi order otomatis.
"""

def calculate_ma(prices: list, period: int) -> float:
    """Hitung moving average dari list harga (ambil N terakhir)."""
    if len(prices) < period:
        return None
    return sum(prices[-period:]) / period

def generate_signal(prices: list) -> dict:
    """
    Analisa list harga (urut dari lama ke baru) dan kasih sinyal.
    prices: list harga close, minimal 50 data untuk MA50.
    """
    if len(prices) < 50:
        return {"signal": "NOT_ENOUGH_DATA", "ma20": None, "ma50": None}

    ma20_now = calculate_ma(prices, 20)
    ma50_now = calculate_ma(prices, 50)
    ma20_prev = calculate_ma(prices[:-1], 20)
    ma50_prev = calculate_ma(prices[:-1], 50)

    signal = "HOLD"
    if ma20_prev <= ma50_prev and ma20_now > ma50_now:
        signal = "BUY"
    elif ma20_prev >= ma50_prev and ma20_now < ma50_now:
        signal = "SELL"

    return {
        "signal": signal,
        "ma20": round(ma20_now, 2),
        "ma50": round(ma50_now, 2),
    }
