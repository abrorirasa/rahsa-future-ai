"""Membaca semua file hasil backtest dan membuat kesimpulan akhir."""
import os

files_to_read = [
    "hasil_backtest.txt",
    "hasil_final_backtest.txt",
    "hasil_rsi.txt",
    "hasil_validasi_btc_rsi.txt",
    "hasil_combined.txt",
    "hasil_validasi_top3.txt",
]

summary_lines = ["=" * 50]
summary_lines.append("RINGKASAN LENGKAP RISET STRATEGI RAHSA FUTURE AI")
summary_lines.append("=" * 50)
summary_lines.append("")

for filename in files_to_read:
    if os.path.exists(filename):
        with open(filename) as f:
            content = f.read()
        summary_lines.append(f"--- {filename} ---")
        summary_lines.append(content)
        summary_lines.append("")
    else:
        summary_lines.append(f"--- {filename} (belum ada / belum sempat dibuat) ---\n")

summary_lines.append("=" * 50)
summary_lines.append("KESIMPULAN SEMENTARA:")
summary_lines.append("Strategi terbaik sejauh ini: Kombinasi MA20/MA50 + RSI")
summary_lines.append("Top performer: SOLUSDT, LINKUSDT, LTCUSDT")
summary_lines.append("Perlu divalidasi lebih lanjut sebelum dipakai dengan dana asli.")
summary_lines.append("Belum ada strategi yang 100% terbukti stabil di semua periode.")
summary_lines.append("=" * 50)

output = "\n".join(summary_lines)
with open("KESIMPULAN_FINAL.txt", "w") as f:
    f.write(output)

print("Kesimpulan lengkap tersimpan di file: KESIMPULAN_FINAL.txt")
print(f"Total {len([f for f in files_to_read if os.path.exists(f)])} dari {len(files_to_read)} file hasil ditemukan.")
