"""
Backtesting Engine - Rahsa Future AI
Menguji strategi MA20/MA50 ke data historis untuk melihat performa
statistiknya (winrate, profit/loss, drawdown). BUKAN jaminan hasil masa depan.
"""

def run_backtest(prices: list, initial_capital: float = 1000.0) -> dict:
    """
    Simulasikan strategi MA20/MA50 crossover terhadap data harga historis.
    prices: list harga urut dari lama ke baru.
    """
    from trading_engine.strategy import calculate_ma

    capital = initial_capital
    position = None
    entry_price = 0
    trades = []

    for i in range(50, len(prices)):
        window = prices[:i+1]
        ma20_now = calculate_ma(window, 20)
        ma50_now = calculate_ma(window, 50)
        ma20_prev = calculate_ma(window[:-1], 20)
        ma50_prev = calculate_ma(window[:-1], 50)
        price_now = prices[i]

        if position is None and ma20_prev <= ma50_prev and ma20_now > ma50_now:
            position = "LONG"
            entry_price = price_now
        elif position == "LONG" and ma20_prev >= ma50_prev and ma20_now < ma50_now:
            pnl_percent = (price_now - entry_price) / entry_price * 100
            capital *= (1 + pnl_percent / 100)
            trades.append(pnl_percent)
            position = None

    wins = [t for t in trades if t > 0]
    losses = [t for t in trades if t <= 0]
    winrate = (len(wins) / len(trades) * 100) if trades else 0

    return {
        "total_trades": len(trades),
        "winrate_percent": round(winrate, 2),
        "final_capital": round(capital, 2),
        "return_percent": round((capital - initial_capital) / initial_capital * 100, 2),
        "avg_win_percent": round(sum(wins) / len(wins), 2) if wins else 0,
        "avg_loss_percent": round(sum(losses) / len(losses), 2) if losses else 0,
    }
