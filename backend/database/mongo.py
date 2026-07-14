"""
Koneksi MongoDB - untuk data pasar mentah & data AI learning
(sesuai Implementation Decision Notes #1: Hybrid Database Architecture).

Koleksi yang dipakai:
- market_data_raw   : harga & volume mentah dari exchange
- ai_decision_log   : histori keputusan AI beserta alasan (explainability)
- system_events     : log tak terstruktur (opsional, pelengkap SystemLog di Postgres)
"""
from motor.motor_asyncio import AsyncIOMotorClient
from backend.core.config import settings

_client = AsyncIOMotorClient(settings.MONGO_URI)
mongo_db = _client[settings.MONGO_DB]

market_data_raw = mongo_db["market_data_raw"]
ai_decision_log = mongo_db["ai_decision_log"]
system_events = mongo_db["system_events"]
