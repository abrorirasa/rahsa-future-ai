"""
Risk Management Engine - Rahsa Future AI
Sesuai Implementation Decision Notes:
- Maksimal 3 posisi simultan
- Maksimal risiko 2% modal per posisi
- Ada batas rugi harian untuk hentikan trading otomatis
"""

class RiskManager:
    def __init__(self, capital: float, max_positions: int = 3,
                 max_risk_percent: float = 2.0, max_daily_loss_percent: float = 5.0):
        self.capital = capital
        self.max_positions = max_positions
        self.max_risk_percent = max_risk_percent
        self.max_daily_loss_percent = max_daily_loss_percent
        self.open_positions = 0
        self.daily_pnl_percent = 0.0
        self.trading_halted = False

    def can_open_position(self) -> dict:
        """Cek apakah boleh buka posisi baru."""
        if self.trading_halted:
            return {"allowed": False, "reason": "Trading dihentikan: batas rugi harian tercapai"}
        if self.open_positions >= self.max_positions:
            return {"allowed": False, "reason": f"Sudah mencapai batas maksimal {self.max_positions} posisi"}
        return {"allowed": True, "reason": "OK"}

    def calculate_position_size(self) -> float:
        """Hitung besar modal yang boleh dipakai untuk 1 posisi (berbasis risk %)."""
        return round(self.capital * (self.max_risk_percent / 100), 2)

    def register_trade_result(self, pnl_percent: float):
        """Catat hasil trade (untung/rugi) dan update status harian."""
        self.daily_pnl_percent += pnl_percent
        self.open_positions = max(0, self.open_positions - 1)

        if self.daily_pnl_percent <= -self.max_daily_loss_percent:
            self.trading_halted = True

    def open_position(self):
        self.open_positions += 1

    def reset_daily(self):
        """Panggil ini di awal hari baru."""
        self.daily_pnl_percent = 0.0
        self.trading_halted = False
