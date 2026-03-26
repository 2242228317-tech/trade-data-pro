from sqlalchemy import create_engine, Column, String, Float, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Stock(Base):
    __tablename__ = "stocks"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), index=True)
    name = Column(String(100))
    price = Column(Float)
    change_percent = Column(Float)
    volume = Column(Float)
    amount = Column(Float)
    turnover_ratio = Column(Float)
    market_cap = Column(Float)
    updated_at = Column(DateTime, default=datetime.now)

class Watchlist(Base):
    __tablename__ = "watchlist"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), index=True)
    name = Column(String(100))
    added_at = Column(DateTime, default=datetime.now)

class Strategy(Base):
    __tablename__ = "strategies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    type = Column(String(50))  # ma_cross, macd, kdj, boll
    params = Column(String(500))  # JSON string
    created_at = Column(DateTime, default=datetime.now)

class TradeSignal(Base):
    __tablename__ = "trade_signals"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), index=True)
    strategy = Column(String(50))
    signal = Column(String(10))  # BUY, SELL, HOLD
    price = Column(Float)
    created_at = Column(DateTime, default=datetime.now)

# 数据库连接
DATABASE_URL = "sqlite:///./quant_trading.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
