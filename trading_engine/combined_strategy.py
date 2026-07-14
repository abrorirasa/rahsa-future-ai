"""Strategi Gabungan: MA20/MA50 + RSI. Sinyal BUY hanya jika kedua indikator setuju."""
from trading_engine.strategy import generate_signal
from trading_engine.rsi_strategy import generate_rsi_signal

def generate_combined_signal(prices: list) -> dict:
    ma_result = generate_signal(prices)
    rsi_result = generate_rsi_signal(prices)

    if ma_result["signal"] == "NOT_ENOUGH_DATA" or rsi_result["signal"] == "NOT_ENOUGH_DATA":
        return {"signal": "NOT_ENOUGH_DATA"}

    signal = "HOLD"
    if ma_result["signal"] == "BUY" and rsi_result["rsi"] < 50:
        signal = "BUY"
    elif ma_result["signal"] == "SELL" and rsi_result["rsi"] > 50:
        signal = "SELL"
    elif rsi_result["signal"] == "BUY":
        signal = "BUY"
    elif rsi_result["signal"] == "SELL":
        signal = "SELL"

    return {"signal": signal, "ma20": ma_result.get("ma20"), "ma50": ma_result.get("ma50"), "rsi": rsi_result["rsi"]}
