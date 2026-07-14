"""
Database models (PostgreSQL) - Rahsa Future AI

Menyimpan data transaksional: user, akun trading, posisi, order, log risiko.
Data pasar mentah & data AI learning disimpan terpisah di MongoDB
(lihat backend/database/mongo.py).
"""
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, Enum
)
from sqlalchemy.orm import relationship, declarative_base
import enum

Base = declarative_base()


class PositionStatus(str, enum.Enum):
    OPEN = "open"
    CLOSED = "closed"
    CANCELLED = "cancelled"


class OrderSide(str, enum.Enum):
    BUY = "buy"
    SELL = "sell"


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELLED = "cancelled"
    FAILED = "failed"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    trading_accounts = relationship("TradingAccount", back_populates="owner")


class TradingAccount(Base):
    """
    Akun trading milik user untuk exchange tertentu.
    Kredensial API TIDAK disimpan di sini secara plaintext -
    hanya referensi ke secret manager / env (lihat Implementation Decision Notes #11).
    """
    __tablename__ = "trading_accounts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    exchange = Column(String(32), default="binance")
    is_testnet = Column(Boolean, default=True)
    status = Column(String(16), default="active")  # active, disabled, emergency_stop
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="trading_accounts")
    positions = relationship("Position", back_populates="account")
    orders = relationship("Order", back_populates="account")


class Position(Base):
    """Posisi trading (satu entry sampai ditutup)."""
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("trading_accounts.id"), nullable=False)
    symbol = Column(String(20), nullable=False)  # contoh: BTCUSDT
    side = Column(Enum(OrderSide), nullable=False)
    entry_price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    stop_loss_price = Column(Float, nullable=True)
    take_profit_price = Column(Float, nullable=True)
    status = Column(Enum(PositionStatus), default=PositionStatus.OPEN)
    opened_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)
    close_price = Column(Float, nullable=True)
    realized_pnl = Column(Float, nullable=True)
    strategy_name = Column(String(64), default="MA20_MA50_CROSSOVER")

    account = relationship("TradingAccount", back_populates="positions")


class Order(Base):
    """Order individual yang dikirim ke exchange (termasuk partial fill tracking)."""
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("trading_accounts.id"), nullable=False)
    position_id = Column(Integer, ForeignKey("positions.id"), nullable=True)
    exchange_order_id = Column(String(64), nullable=True)
    symbol = Column(String(20), nullable=False)
    side = Column(Enum(OrderSide), nullable=False)
    order_type = Column(String(16), default="market")  # market, limit, stop_loss
    requested_quantity = Column(Float, nullable=False)
    filled_quantity = Column(Float, default=0)
    price = Column(Float, nullable=True)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    account = relationship("TradingAccount", back_populates="orders")


class RiskEvent(Base):
    """
    Log setiap kali risk management melakukan intervensi
    (block order, trigger stop loss, halt trading, dsb).
    Wajib ada untuk audit trail (lihat dokumen 007 & 012).
    """
    __tablename__ = "risk_events"

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("trading_accounts.id"), nullable=False)
    event_type = Column(String(64), nullable=False)  # e.g. "max_position_reached"
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class SystemLog(Base):
    """Log umum sistem (koneksi exchange gagal, restart, dsb) - untuk failsafe/recovery."""
    __tablename__ = "system_logs"

    id = Column(Integer, primary_key=True)
    level = Column(String(16), default="INFO")  # INFO, WARNING, ERROR, CRITICAL
    source = Column(String(64), nullable=False)  # e.g. "exchange_connector"
    message = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
