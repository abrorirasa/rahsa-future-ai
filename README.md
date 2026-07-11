# RAHSA FUTURE AI - V1 (Foundation)

Personal AI Trading Assistant & Automated Trading Bot.

Status: **Phase 0 - Foundation Development**

## Filosofi

Dibangun bertahap, diuji tiap tahap, tidak menyentuh dana asli sebelum
terbukti stabil di mode simulasi. Lihat `docs/IMPLEMENTATION_DECISION_NOTES.md`
untuk semua keputusan teknis yang mendasari struktur ini.

## Struktur Proyek

```
RAHSA-FUTURE-AI-V1/
├── backend/
│   ├── main.py              # Entry point aplikasi (FastAPI)
│   ├── api/                 # Endpoint REST API
│   ├── core/                # Config, logging, settings
│   └── database/            # Model & koneksi database
├── trading_engine/          # Strategi, sinyal, eksekusi simulasi
├── ai_engine/                # Scoring & analisis
├── exchange/                 # Konektor ke Binance
├── data/                     # (kosong, untuk data lokal/cache)
├── docs/                     # Dokumentasi teknis proyek
├── tests/                    # Unit test
└── requirements.txt
```

## Tech Stack (sesuai Implementation Decision Notes)

- **Bahasa**: Python 3.11+
- **API Framework**: FastAPI
- **Database**: PostgreSQL (data transaksional) + MongoDB (data pasar/AI)
- **Real-time**: WebSocket (untuk data live) + REST (untuk command)
- **Exchange**: Binance (Phase 1)

## Roadmap Pembangunan

- [x] Phase 0 - Foundation (struktur proyek, environment)
- [ ] Phase 1 - Core Backend (API + Database hidup)
- [ ] Phase 2 - Market Data Engine (koneksi exchange, ambil harga)
- [ ] Phase 3 - Trading Simulator (MA20/MA50, paper trading)
- [ ] Phase 4 - Risk Management Engine
- [ ] Phase 5 - AI Scoring Engine
- [ ] Phase 6 - Dashboard & Monitoring

## Catatan Penting

⚠️ Sistem ini BELUM boleh dihubungkan ke akun exchange dengan dana asli
sampai seluruh Phase 1-4 selesai diuji di mode simulasi.
