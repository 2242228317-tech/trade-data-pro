from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, timedelta

from ..services.data_service import data_service
from ..services.indicator_service import indicator_service
from ..services.strategy_service import strategy_service
from ..services.backtest_service import backtest_service

router = APIRouter(prefix="/api/backtest", tags=["backtest"])

class BacktestRequest(BaseModel):
    code: str
    strategy_type: str = "ma_cross"
    initial_capital: float = 100000
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    commission_rate: float = 0.0003
    stop_loss: float = 0.08

class BacktestResponse(BaseModel):
    code: str
    strategy: str
    initial_capital: float
    final_capital: float
    total_return_pct: float
    total_trades: int
    win_rate: float
    max_drawdown_pct: float
    sharpe_ratio: float

@router.post("/run")
def run_backtest(request: BacktestRequest):
    """运行策略回测"""
    # 获取历史数据
    if request.end_date is None:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(request.end_date, '%Y-%m-%d')
    
    if request.start_date is None:
        start_date = end_date - timedelta(days=730)  # 默认2年
    else:
        start_date = datetime.strptime(request.start_date, '%Y-%m-%d')
    
    df = data_service.get_daily_data(
        request.code,
        start_date=start_date.strftime('%Y%m%d'),
        end_date=end_date.strftime('%Y%m%d')
    )
    
    if df.empty or len(df) < 60:
        raise HTTPException(status_code=404, detail=f"Insufficient data for {request.code}")
    
    # 计算技术指标
    df = indicator_service.calculate_all(df)
    
    # 获取策略函数
    strategy_func = lambda x: strategy_service.run_strategy(x, request.strategy_type)
    
    # 运行回测
    result = backtest_service.run_backtest(
        df, 
        strategy_func,
        initial_capital=request.initial_capital,
        commission_rate=request.commission_rate,
        stop_loss=request.stop_loss
    )
    
    # 格式化交易记录
    trades = []
    for trade in result.trades:
        trades.append({
            "date": trade.date.strftime('%Y-%m-%d') if isinstance(trade.date, datetime) else str(trade.date),
            "action": trade.action,
            "price": trade.price,
            "shares": trade.shares,
            "amount": trade.amount,
            "reason": trade.reason
        })
    
    # 格式化权益曲线
    equity_curve = []
    for point in result.equity_curve:
        equity_curve.append({
            "date": point['date'].strftime('%Y-%m-%d') if isinstance(point['date'], datetime) else str(point['date']),
            "equity": point['equity'],
            "price": point['price'],
            "signal": point['signal']
        })
    
    return {
        "code": request.code,
        "strategy": request.strategy_type,
        "initial_capital": result.initial_capital,
        "final_capital": round(result.final_capital, 2),
        "total_return": round(result.total_return, 2),
        "total_return_pct": round(result.total_return_pct, 2),
        "total_trades": result.total_trades,
        "winning_trades": result.winning_trades,
        "losing_trades": result.losing_trades,
        "win_rate": round(result.win_rate, 2),
        "max_drawdown": round(result.max_drawdown, 2),
        "max_drawdown_pct": round(result.max_drawdown_pct, 2),
        "sharpe_ratio": round(result.sharpe_ratio, 2),
        "trades": trades,
        "equity_curve": equity_curve
    }

@router.get("/compare/{code}")
def compare_strategies(
    code: str,
    days: int = Query(365, ge=60, le=2000)
):
    """对比多个策略的回测表现"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    df = data_service.get_daily_data(
        code,
        start_date=start_date.strftime('%Y%m%d'),
        end_date=end_date.strftime('%Y%m%d')
    )
    
    if df.empty or len(df) < 60:
        raise HTTPException(status_code=404, detail=f"Insufficient data for {code}")
    
    df = indicator_service.calculate_all(df)
    
    strategies = {
        'MA交叉': lambda x: strategy_service.ma_cross_strategy(x),
        'MACD': lambda x: strategy_service.macd_strategy(x),
        'KDJ': lambda x: strategy_service.kdj_strategy(x),
        '布林带': lambda x: strategy_service.boll_strategy(x),
        'RSI': lambda x: strategy_service.rsi_strategy(x),
        '综合策略': lambda x: strategy_service.combined_strategy(x)
    }
    
    results = backtest_service.compare_strategies(df, strategies)
    
    return {
        "code": code,
        "period": f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
        "comparison": results
    }

@router.get("/monte-carlo/{code}")
def monte_carlo_simulation(
    code: str,
    strategy_type: str = Query("ma_cross", enum=["ma_cross", "macd", "kdj", "boll", "rsi", "combined"]),
    runs: int = Query(100, ge=10, le=500)
):
    """蒙特卡洛模拟风险评估"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    df = data_service.get_daily_data(
        code,
        start_date=start_date.strftime('%Y%m%d'),
        end_date=end_date.strftime('%Y%m%d')
    )
    
    if df.empty or len(df) < 60:
        raise HTTPException(status_code=404, detail=f"Insufficient data for {code}")
    
    strategy_func = lambda x: strategy_service.run_strategy(x, strategy_type)
    
    result = backtest_service.monte_carlo_simulation(df, strategy_func, runs=runs)
    
    return {
        "code": code,
        "strategy": strategy_type,
        "simulation_runs": runs,
        "expected_return_pct": round(result['expected_return'], 2),
        "return_std": round(result['return_std'], 2),
        "worst_case_pct": round(result['worst_case'], 2),
        "best_case_pct": round(result['best_case'], 2),
        "var_95_pct": round(result['var_95'], 2),
        "expected_max_drawdown_pct": round(result['expected_max_drawdown'], 2),
        "worst_drawdown_pct": round(result['worst_drawdown'], 2),
        "risk_assessment": "HIGH" if result['var_95'] < -20 else ("MEDIUM" if result['var_95'] < -10 else "LOW")
    }

@router.get("/optimize/{code}")
def optimize_parameters(
    code: str,
    strategy_type: str = Query("ma_cross", enum=["ma_cross", "macd"])
):
    """策略参数优化"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    df = data_service.get_daily_data(
        code,
        start_date=start_date.strftime('%Y%m%d'),
        end_date=end_date.strftime('%Y%m%d')
    )
    
    if df.empty or len(df) < 60:
        raise HTTPException(status_code=404, detail=f"Insufficient data for {code}")
    
    df = indicator_service.calculate_all(df)
    
    best_return = -float('inf')
    best_params = {}
    
    if strategy_type == "ma_cross":
        # 测试不同的均线组合
        for short in [5, 10, 15]:
            for long in [20, 30, 60]:
                if short >= long:
                    continue
                
                def strategy_func(x):
                    return strategy_service.ma_cross_strategy(x, short, long)
                
                result = backtest_service.run_backtest(df, strategy_func)
                
                if result.total_return_pct > best_return:
                    best_return = result.total_return_pct
                    best_params = {"short": short, "long": long}
    
    elif strategy_type == "macd":
        # MACD参数优化
        for short in [10, 12, 15]:
            for long in [20, 26, 30]:
                for signal in [7, 9, 12]:
                    if short >= long:
                        continue
                    
                    def strategy_func(x):
                        df_copy = x.copy()
                        ema_short = indicator_service.ema(df_copy['close'], short)
                        ema_long = indicator_service.ema(df_copy['close'], long)
                        diff = ema_short - ema_long
                        dea = indicator_service.ema(diff, signal)
                        macd_val = (diff - dea) * 2
                        
                        latest = df_copy.iloc[-1]
                        prev = df_copy.iloc[-2]
                        
                        if diff.iloc[-1] > dea.iloc[-1] and diff.iloc[-2] <= dea.iloc[-2]:
                            return {"signal": "BUY", "price": latest['close']}
                        elif diff.iloc[-1] < dea.iloc[-1] and diff.iloc[-2] >= dea.iloc[-2]:
                            return {"signal": "SELL", "price": latest['close']}
                        return {"signal": "HOLD", "price": latest['close']}
                    
                    result = backtest_service.run_backtest(df, strategy_func)
                    
                    if result.total_return_pct > best_return:
                        best_return = result.total_return_pct
                        best_params = {"short": short, "long": long, "signal": signal}
    
    return {
        "code": code,
        "strategy": strategy_type,
        "best_params": best_params,
        "expected_return_pct": round(best_return, 2)
    }
