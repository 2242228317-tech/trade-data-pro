from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta

from ..services.data_service import data_service
from ..services.indicator_service import indicator_service
from ..services.strategy_service import strategy_service

router = APIRouter(prefix="/api/strategy", tags=["strategy"])

class StrategyRequest(BaseModel):
    code: str
    strategy_type: str = "combined"  # ma_cross, macd, kdj, boll, rsi, combined
    params: Optional[dict] = None

class StrategyResponse(BaseModel):
    code: str
    strategy: str
    signal: str
    reason: str
    price: float
    strength: float

@router.get("/{code}/signal")
def get_strategy_signal(
    code: str,
    strategy_type: str = Query("combined", enum=["ma_cross", "macd", "kdj", "boll", "rsi", "combined"])
):
    """获取策略信号"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=100)
    
    df = data_service.get_daily_data(
        code,
        start_date=start_date.strftime('%Y%m%d'),
        end_date=end_date.strftime('%Y%m%d')
    )
    
    if df.empty or len(df) < 30:
        raise HTTPException(status_code=404, detail=f"Insufficient data for {code}")
    
    # 计算技术指标
    df = indicator_service.calculate_all(df)
    
    # 运行策略
    result = strategy_service.run_strategy(df, strategy_type)
    
    return {
        "code": code,
        "strategy": strategy_type,
        "signal": result.get("signal", "HOLD"),
        "reason": result.get("reason", ""),
        "price": result.get("price", 0),
        "strength": result.get("strength", 0),
        "timestamp": datetime.now().isoformat()
    }

@router.get("/{code}/all-signals")
def get_all_strategy_signals(code: str):
    """获取所有策略的信号对比"""
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
    
    strategies = ["ma_cross", "macd", "kdj", "boll", "rsi", "combined"]
    signals = {}
    
    for strategy in strategies:
        result = strategy_service.run_strategy(df, strategy)
        signals[strategy] = {
            "signal": result.get("signal", "HOLD"),
            "reason": result.get("reason", ""),
            "strength": result.get("strength", 0)
        }
    
    # 统计
    buy_count = sum(1 for s in signals.values() if s["signal"] == "BUY")
    sell_count = sum(1 for s in signals.values() if s["signal"] == "SELL")
    
    latest = df.iloc[-1]
    
    return {
        "code": code,
        "date": df.index[-1].strftime('%Y-%m-%d'),
        "price": float(latest['close']),
        "signals": signals,
        "summary": {
            "buy_signals": buy_count,
            "sell_signals": sell_count,
            "consensus": "BUY" if buy_count >= 3 else ("SELL" if sell_count >= 3 else "NEUTRAL")
        }
    }

@router.get("/scan/buy-signals")
def scan_buy_signals(
    strategy_type: str = Query("combined", enum=["ma_cross", "macd", "kdj", "boll", "rsi", "combined"]),
    limit: int = Query(20, ge=1, le=100)
):
    """扫描全市场买入信号"""
    # 获取高流动性股票池
    df = data_service.filter_stocks(min_volume=15000000, min_amount=1, min_turnover=3)
    
    if df.empty:
        return {"signals": [], "count": 0}
    
    buy_signals = []
    
    for _, row in df.head(limit * 2).iterrows():  # 扫描更多以过滤
        code = row.get("code", "")
        if not code:
            continue
        
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=100)
            
            hist_df = data_service.get_daily_data(
                code,
                start_date=start_date.strftime('%Y%m%d'),
                end_date=end_date.strftime('%Y%m%d')
            )
            
            if hist_df.empty or len(hist_df) < 30:
                continue
            
            hist_df = indicator_service.calculate_all(hist_df)
            result = strategy_service.run_strategy(hist_df, strategy_type)
            
            if result.get("signal") in ["BUY", "WEAK_BUY"]:
                buy_signals.append({
                    "code": code,
                    "name": row.get("name", ""),
                    "price": float(row.get("trade", 0)),
                    "change_percent": float(row.get("changepercent", 0)),
                    "turnover_ratio": float(row.get("turnoverratio", 0)),
                    "signal": result.get("signal"),
                    "reason": result.get("reason"),
                    "strength": result.get("strength", 0)
                })
                
                if len(buy_signals) >= limit:
                    break
                    
        except Exception as e:
            continue
    
    # 按信号强度排序
    buy_signals.sort(key=lambda x: x["strength"], reverse=True)
    
    return {
        "strategy": strategy_type,
        "signals": buy_signals,
        "count": len(buy_signals),
        "timestamp": datetime.now().isoformat()
    }

@router.get("/scan/sell-signals")
def scan_sell_signals(
    strategy_type: str = Query("combined", enum=["ma_cross", "macd", "kdj", "boll", "rsi", "combined"]),
    limit: int = Query(20, ge=1, le=100)
):
    """扫描全市场卖出信号"""
    df = data_service.filter_stocks(min_volume=15000000, min_amount=1, min_turnover=3)
    
    if df.empty:
        return {"signals": [], "count": 0}
    
    sell_signals = []
    
    for _, row in df.head(limit * 2).iterrows():
        code = row.get("code", "")
        if not code:
            continue
        
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=100)
            
            hist_df = data_service.get_daily_data(
                code,
                start_date=start_date.strftime('%Y%m%d'),
                end_date=end_date.strftime('%Y%m%d')
            )
            
            if hist_df.empty or len(hist_df) < 30:
                continue
            
            hist_df = indicator_service.calculate_all(hist_df)
            result = strategy_service.run_strategy(hist_df, strategy_type)
            
            if result.get("signal") in ["SELL", "WEAK_SELL"]:
                sell_signals.append({
                    "code": code,
                    "name": row.get("name", ""),
                    "price": float(row.get("trade", 0)),
                    "change_percent": float(row.get("changepercent", 0)),
                    "turnover_ratio": float(row.get("turnoverratio", 0)),
                    "signal": result.get("signal"),
                    "reason": result.get("reason"),
                    "strength": result.get("strength", 0)
                })
                
                if len(sell_signals) >= limit:
                    break
                    
        except Exception as e:
            continue
    
    sell_signals.sort(key=lambda x: x["strength"], reverse=True)
    
    return {
        "strategy": strategy_type,
        "signals": sell_signals,
        "count": len(sell_signals),
        "timestamp": datetime.now().isoformat()
    }

@router.get("/hot-stocks")
def get_hot_stocks(limit: int = Query(20, ge=1, le=50)):
    """获取热门股票（高换手率+上涨）"""
    df = data_service.filter_stocks(min_volume=15000000, min_amount=1, min_turnover=5)
    
    if df.empty:
        return {"stocks": [], "count": 0}
    
    # 筛选上涨的
    df = df[df['changepercent'] > 0]
    df = df.sort_values(by='turnoverratio', ascending=False)
    
    stocks = []
    for _, row in df.head(limit).iterrows():
        stocks.append({
            "code": row.get("code", ""),
            "name": row.get("name", ""),
            "price": float(row.get("trade", 0)),
            "change_percent": float(row.get("changepercent", 0)),
            "turnover_ratio": float(row.get("turnoverratio", 0)),
            "volume": float(row.get("volume", 0)),
            "amount": float(row.get("amount_yi", 0))
        })
    
    return {"stocks": stocks, "count": len(stocks)}
