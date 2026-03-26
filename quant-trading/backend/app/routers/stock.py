from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from ..models import get_db
from ..services.data_service import data_service
from ..services.indicator_service import indicator_service
from ..services.strategy_service import strategy_service
from ..services.backtest_service import backtest_service

router = APIRouter(prefix="/api/stocks", tags=["stocks"])

class StockResponse(BaseModel):
    code: str
    name: str
    price: float
    change_percent: float
    volume: float
    amount: float
    turnover_ratio: float
    market_cap: float

class StockDetail(BaseModel):
    code: str
    name: str
    price: float
    change_percent: float
    volume: float
    amount: float
    turnover_ratio: float
    market_cap: float
    industry: Optional[str] = None
    area: Optional[str] = None

@router.get("/realtime", response_model=List[StockResponse])
def get_realtime_stocks(
    limit: int = Query(50, ge=1, le=500),
    min_turnover: float = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """获取实时股票数据"""
    df = data_service.get_realtime_data()
    if df.empty:
        return []
    
    if min_turnover > 0:
        df = df[df["turnoverratio"] > min_turnover]
    
    df = df.head(limit)
    
    results = []
    for _, row in df.iterrows():
        results.append({
            "code": row.get("code", ""),
            "name": row.get("name", ""),
            "price": float(row.get("trade", 0)),
            "change_percent": float(row.get("changepercent", 0)),
            "volume": float(row.get("volume", 0)),
            "amount": float(row.get("amount", 0)),
            "turnover_ratio": float(row.get("turnoverratio", 0)),
            "market_cap": float(row.get("nmc", 0))
        })
    
    return results

@router.get("/filtered")
def get_filtered_stocks(
    min_volume: float = Query(15000000, ge=0),
    min_amount: float = Query(1, ge=0),
    min_turnover: float = Query(3, ge=0)
):
    """筛选股票：高流动性股票"""
    df = data_service.filter_stocks(min_volume, min_amount, min_turnover)
    if df.empty:
        return {"stocks": [], "count": 0}
    
    stocks = []
    for _, row in df.iterrows():
        stocks.append({
            "code": row.get("code", ""),
            "name": row.get("name", ""),
            "price": float(row.get("trade", 0)),
            "change_percent": float(row.get("changepercent", 0)),
            "volume": float(row.get("volume", 0)),
            "amount": float(row.get("amount_yi", 0)),
            "turnover_ratio": float(row.get("turnoverratio", 0)),
            "market_cap": float(row.get("nmc", 0))
        })
    
    return {"stocks": stocks, "count": len(stocks)}

@router.get("/{code}/history")
def get_stock_history(
    code: str,
    days: int = Query(365, ge=30, le=2000)
):
    """获取股票历史数据"""
    from datetime import timedelta
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    df = data_service.get_daily_data(
        code, 
        start_date=start_date.strftime('%Y%m%d'),
        end_date=end_date.strftime('%Y%m%d')
    )
    
    if df.empty:
        raise HTTPException(status_code=404, detail=f"Stock {code} not found")
    
    data = []
    for index, row in df.iterrows():
        data.append({
            "date": index.strftime('%Y-%m-%d'),
            "open": float(row.get("open", 0)),
            "high": float(row.get("high", 0)),
            "low": float(row.get("low", 0)),
            "close": float(row.get("close", 0)),
            "volume": float(row.get("vol", 0)),
            "amount": float(row.get("amount", 0))
        })
    
    return {
        "code": code,
        "data": data,
        "count": len(data)
    }

@router.get("/{code}/info")
def get_stock_info(code: str):
    """获取股票基本信息"""
    df = data_service.get_stock_basic()
    if df.empty:
        raise HTTPException(status_code=503, detail="Stock basic data unavailable")
    
    stock = df[df['symbol'] == code.replace('.XSHG', '').replace('.XSHE', '')]
    if stock.empty:
        raise HTTPException(status_code=404, detail=f"Stock {code} not found")
    
    row = stock.iloc[0]
    return {
        "code": row.get("symbol", ""),
        "name": row.get("name", ""),
        "industry": row.get("industry", ""),
        "area": row.get("area", ""),
        "list_date": row.get("list_date", "")
    }

@router.get("/{code}/moneyflow")
def get_money_flow(code: str):
    """获取资金流向数据"""
    flow = data_service.get_money_flow(code)
    return {
        "code": code,
        "money_flow": flow
    }
