"""Strategi RSI - beli saat oversold, jual saat overbought."""

def calculate_rsi(prices: list, period: int = 14) -> float:
    if len(prices) < period + 1:
        return None
    gains, losses = [], []
    for i in range(-period, 0):
        change = prices[i] - prices[i-1]
        gains.append(max(change, 0))
        losses.append(max(-change, 0))
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def generate_rsi_signal(prices: list, oversold=30, overbought=70) -> dict:
    if len(prices) < 15:
        return {"signal": "NOT_ENOUGH_DATA", "rsi": None}
    rsi = calculate_rsi(prices)
    signal = "HOLD"
    if rsi <= oversold:
        signal = "BUY"
    elif rsi >= overbought:
        signal = "SELL"
    return {"signal": signal, "rsi": round(rsi, 2)}
