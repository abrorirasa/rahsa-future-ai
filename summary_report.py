"""Membaca hasil_final_backtest.txt dan menyajikan ringkasan yang gampang dibaca."""
with open("hasil_final_backtest.txt") as f:
    content = f.read()

print(content)
print("\n=== ANALISIS ===")
lines = [l for l in content.split("\n") if "trade" in l and "PnL" in l]
best_pnl = None
best_line = ""
for line in lines:
    try:
        pnl_str = line.split("total PnL ")[1].replace("%", "")
        pnl = float(pnl_str)
        if best_pnl is None or pnl > best_pnl:
            best_pnl = pnl
            best_line = line
    except:
        continue
print(f"Koin dengan performa terbaik: {best_line}")
