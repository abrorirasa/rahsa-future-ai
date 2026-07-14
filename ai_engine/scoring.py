"""
AI Scoring Engine V1 - Rule-Based Scoring (bukan Machine Learning dulu)
Sesuai Implementation Decision Notes: mulai dari sistem transparan & mudah diuji.
"""

def calculate_trend_score(prices: list) -> int:
    """Skor trend: makin konsisten naik, makin tinggi skornya (-30 s/d +30)."""
    if len(prices) < 10:
        return 0
    recent = prices[-10:]
    ups = sum(1 for i in range(1, len(recent)) if recent[i] > recent[i-1])
    return round((ups / 9) * 60 - 30)

def calculate_volume_score(volumes: list) -> int:
    """Skor volume: volume naik dibanding rata-rata = sinyal lebih kuat (0 s/d +20)."""
    if len(volumes) < 10:
        return 0
    avg_vol = sum(volumes[-10:-1]) / 9
    current_vol = volumes[-1]
    if avg_vol == 0:
        return 0
    ratio = current_vol / avg_vol
    return min(20, round((ratio - 1) * 20))

def calculate_momentum_score(prices: list) -> int:
    """Skor momentum: seberapa jauh harga bergerak dalam waktu singkat (-20 s/d +20)."""
    if len(prices) < 5:
        return 0
    change_pct = (prices[-1] - prices[-5]) / prices[-5] * 100
    return max(-20, min(20, round(change_pct * 4)))

def calculate_final_score(prices: list, volumes: list, ma_signal: str) -> dict:
    """
    Gabungkan semua skor jadi satu keputusan akhir.
    ma_signal: "BUY", "SELL", atau "HOLD" dari strategy.py
    """
    trend = calculate_trend_score(prices)
    volume = calculate_volume_score(volumes)
    momentum = calculate_momentum_score(prices)

    base_score = trend + volume + momentum

    if ma_signal == "BUY":
        base_score += 20
    elif ma_signal == "SELL":
        base_score -= 20

    if base_score >= 40:
        decision = "STRONG_BUY"
    elif base_score >= 15:
        decision = "BUY"
    elif base_score <= -40:
        decision = "STRONG_SELL"
    elif base_score <= -15:
        decision = "SELL"
    else:
        decision = "HOLD"

    return {
        "decision": decision,
        "final_score": base_score,
        "breakdown": {
            "trend_score": trend,
            "volume_score": volume,
            "momentum_score": momentum,
            "ma_signal_bonus": 20 if ma_signal == "BUY" else (-20 if ma_signal == "SELL" else 0),
        }
    }
