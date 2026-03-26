from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta

from ..services.data_service import data_service
from ..services.indicator_service import indicator_service

router = APIRouter(prefix="/api/indicators", tags=["indicators"])

class IndicatorRequest(BaseModel):
    code: str
    period: int = 365
    indicators: List[str] = ["ma", "macd", "kdj", "boll", "rsi"]

class IndicatorData(BaseModel):
    date: str
    ma5: Optional[float] = None
    ma10: Optional[float] = None
    ma20: Optional[float] = None
    ma30: Optional[float] = None
    ma60: Optional[float] = None
    macd_diff: Optional[float] = None
    macd_dea: Optional[float] = None
    macd: Optional[float] = None
    kdj_k: Optional[float] = None
    kdj_d: Optional[float] = None
    kdj_j: Optional[float] = None
    boll_upper: Optional[float] = None
    boll_mid: Optional[float] = None
    boll_lower: Optional[float] = None
    rsi6: Optional[float] = None
    rsi12: Optional[float] = None
    rsi24: Optional[float] = None

@router.get("/{code}/all")
def get_all_indicators(
    code: str,
    days: int = Query(365, ge=30, le=2000)
):
    """获取股票所有技术指标"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    df = data_service.get_daily_data(
        code,
        start_date=start_date.strftime('%Y%m%d'),
        end_date=end_date.strftime('%Y%m%d')
    )
    
    if df.empty:
        raise HTTPException(status_code=404, detail=f"Stock {code} not found")
    
    # 计算所有技术指标
    df = indicator_service.calculate_all(df)
    
    # 获取最新信号
    signals = indicator_service.get_latest_signals(df)
    
    # 格式化数据
    data = []
    for index, row in df.iterrows():
        data.append({
            "date": index.strftime('%Y-%m-%d'),
            "open": float(row.get("open", 0)),
            "high": float(row.get("high", 0)),
            "low": float(row.get("low", 0)),
            "close": float(row.get("close", 0)),
            "volume": float(row.get("vol", 0)),
            "ma5": float(row["ma5"]) if pd.notna(row.get("ma5")) else None,
            "ma10": float(row["ma10"]) if pd.notna(row.get("ma10")) else None,
            "ma20": float(row["ma20"]) if pd.notna(row.get("ma20")) else None,
            "ma30": float(row["ma30"]) if pd.notna(row.get("ma30")) else None,
            "ma60": float(row["ma60"]) if pd.notna(row.get("ma60")) else None,
            "macd_diff": float(row["macd_diff"]) if pd.notna(row.get("macd_diff")) else None,
            "macd_dea": float(row["macd_dea"]) if pd.notna(row.get("macd_dea")) else None,
            "macd": float(row["macd"]) if pd.notna(row.get("macd")) else None,
            "kdj_k": float(row["kdj_k"]) if pd.notna(row.get("kdj_k")) else None,
            "kdj_d": float(row["kdj_d"]) if pd.notna(row.get("kdj_d")) else None,
            "kdj_j": float(row["kdj_j"]) if pd.notna(row.get("kdj_j")) else None,
            "boll_upper": float(row["boll_upper"]) if pd.notna(row.get("boll_upper")) else None,
            "boll_mid": float(row["boll_mid"]) if pd.notna(row.get("boll_mid")) else None,
            "boll_lower": float(row["boll_lower"]) if pd.notna(row.get("boll_lower")) else None,
            "rsi6": float(row["rsi6"]) if pd.notna(row.get("rsi6")) else None,
            "rsi12": float(row["rsi12"]) if pd.notna(row.get("rsi12")) else None,
            "rsi24": float(row["rsi24"]) if pd.notna(row.get("rsi24")) else None,
        })
    
    return {
        "code": code,
        "signals": signals,
        "data": data,
        "count": len(data)
    }

@router.get("/{code}/signals")
def get_latest_signals(code: str):
    """获取最新技术指标信号"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=100)
    
    df = data_service.get_daily_data(
        code,
        start_date=start_date.strftime('%Y%m%d'),
        end_date=end_date.strftime('%Y%m%d')
    )
    
    if df.empty or len(df) < 30:
        raise HTTPException(status_code=404, detail=f"Insufficient data for {code}")
    
    df = indicator_service.calculate_all(df)
    signals = indicator_service.get_latest_signals(df)
    
    latest = df.iloc[-1]
    
    return {
        "code": code,
        "date": df.index[-1].strftime('%Y-%m-%d'),
        "price": float(latest['close']),
        "signals": signals,
        "indicators": {
            "ma5": float(latest['ma5']) if pd.notna(latest.get('ma5')) else None,
            "ma10": float(latest['ma10']) if pd.notna(latest.get('ma10')) else None,
            "ma20": float(latest['ma20']) if pd.notna(latest.get('ma20')) else None,
            "ma60": float(latest['ma60']) if pd.notna(latest.get('ma60')) else None,
            "macd": float(latest['macd']) if pd.notna(latest.get('macd')) else None,
            "macd_diff": float(latest['macd_diff']) if pd.notna(latest.get('macd_diff')) else None,
            "macd_dea": float(latest['macd_dea']) if pd.notna(latest.get('macd_dea')) else None,
            "kdj_k": float(latest['kdj_k']) if pd.notna(latest.get('kdj_k')) else None,
            "kdj_d": float(latest['kdj_d']) if pd.notna(latest.get('kdj_d')) else None,
            "kdj_j": float(latest['kdj_j']) if pd.notna(latest.get('kdj_j')) else None,
            "boll_upper": float(latest['boll_upper']) if pd.notna(latest.get('boll_upper')) else None,
            "boll_mid": float(latest['boll_mid']) if pd.notna(latest.get('boll_mid')) else None,
            "boll_lower": float(latest['boll_lower']) if pd.notna(latest.get('boll_lower')) else None,
            "rsi6": float(latest['rsi6']) if pd.notna(latest.get('rsi6')) else None,
        }
    }

# 导入pandas用于数据检查
import pandas as pd
