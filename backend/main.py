"""
Rahsa Future AI - Entry Point Backend

Phase 0/1 target: sistem hidup, database aktif, API berjalan, logging aktif.
Belum ada koneksi exchange atau trading real di file ini.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.core.config import settings
from backend.core.logger import logger
from backend.database.connection import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting Rahsa Future AI backend | env={settings.APP_ENV}")
    try:
        await init_db()
        logger.info("Database tables verified/created.")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
    yield
    logger.info("Shutting down Rahsa Future AI backend.")


app = FastAPI(
    title="Rahsa Future AI",
    description="Personal AI Trading Assistant & Automated Trading Bot - Backend API",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    return {
        "system": "Rahsa Future AI",
        "status": "alive",
        "phase": "Phase 0/1 - Foundation",
    }


@app.get("/health")
async def health_check():
    """
    Endpoint dasar untuk memastikan sistem hidup.
    Nanti akan diperluas untuk cek koneksi DB & exchange (System Watchdog, dok. 007).
    """
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
