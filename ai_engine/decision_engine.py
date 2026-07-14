"""Decision Engine - Menggabungkan Strategy + AI Scoring + Risk Management jadi satu keputusan final."""
from trading_engine.strategy import generate_signal
from ai_engine.scoring import calculate_final_score

def make_decision(prices: list, volumes: list) -> dict:
    ma_result = generate_signal(prices)
    ai_result = calculate_final_score(prices, volumes, ma_result["signal"])
    return {
        "ma_signal": ma_result["signal"],
        "ai_decision": ai_result["decision"],
        "final_score": ai_result["final_score"],
        "action": ai_result["decision"],
        "reasoning": f"MA signal: {ma_result['signal']}, AI score: {ai_result['final_score']} (trend:{ai_result['breakdown']['trend_score']}, volume:{ai_result['breakdown']['volume_score']}, momentum:{ai_result['breakdown']['momentum_score']})"
    }
