"""
Logging terpusat. Setiap modul penting (exchange connector, trading engine,
risk management) wajib log lewat sini - bagian dari Failsafe & Monitoring
(dokumen 007, BAB 7 - System Watchdog).
"""
import sys
from loguru import logger
from backend.core.config import settings

logger.remove()
logger.add(
    sys.stdout,
    level=settings.LOG_LEVEL,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - {message}",
)
logger.add(
    "data/rahsa_future_ai.log",
    level="INFO",
    rotation="10 MB",
    retention="30 days",
)

__all__ = ["logger"]
