from trading_engine.risk_management import RiskManager

rm = RiskManager(capital=1000.0)

print("=== TES RISK MANAGER ===")
print(f"Ukuran posisi per trade (2% modal): ${rm.calculate_position_size()}")

check = rm.can_open_position()
print(f"Boleh buka posisi? {check}")

rm.open_position()
rm.open_position()
rm.open_position()
check2 = rm.can_open_position()
print(f"Setelah 3 posisi dibuka, boleh buka lagi? {check2}")

rm.register_trade_result(-2.0)
rm.register_trade_result(-2.0)
rm.register_trade_result(-1.5)
print(f"PnL harian setelah 3 kali rugi: {rm.daily_pnl_percent}%")
print(f"Trading dihentikan? {rm.trading_halted}")
