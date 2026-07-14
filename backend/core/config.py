"""
Konfigurasi terpusat. Semua nilai sensitif diambil dari environment variables
(.env), TIDAK PERNAH ditulis langsung di kode - sesuai Implementation Decision
Notes #11 (API Key Security Decision).
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"

    # PostgreSQL
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "rahsa_future_ai"
    POSTGRES_USER: str = "rahsa_user"
    POSTGRES_PASSWORD: str = "change_me"

    # MongoDB
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB: str = "rahsa_future_ai_market"

    # Binance
    BINANCE_API_KEY: str = ""
    BINANCE_API_SECRET: str = ""
    BINANCE_TESTNET: bool = True

    # Risk management defaults
    MAX_SIMULTANEOUS_POSITIONS: int = 3
    MAX_RISK_PER_POSITION_PERCENT: float = 2.0


settings = Settings()
