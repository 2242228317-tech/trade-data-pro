import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, field

@dataclass
class Trade:
    """交易记录"""
    date: datetime
    action: str  # BUY, SELL
    price: float
    shares: int
    amount: float
    reason: str = ""

@dataclass
class BacktestResult:
    """回测结果"""
    initial_capital: float
    final_capital: float
    total_return: float
    total_return_pct: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float
    max_drawdown: float
    max_drawdown_pct: float
    sharpe_ratio: float
    trades: List[Trade] = field(default_factory=list)
    equity_curve: List[Dict] = field(default_factory=list)

class BacktestService:
    """回测服务"""
    
    def __init__(self):
        pass
    
    def run_backtest(self, df: pd.DataFrame, strategy_func, 
                     initial_capital: float = 100000,
                     position_size: float = 0.95,
                     commission_rate: float = 0.0003,
                     stop_loss: float = 0.08) -> BacktestResult:
        """
        运行回测
        
        Args:
            df: 股票数据DataFrame
            strategy_func: 策略函数，接收df返回signal字典
            initial_capital: 初始资金
            position_size: 仓位比例
            commission_rate: 手续费率
            stop_loss: 止损比例
        """
        if len(df) < 30:
            return BacktestResult(
                initial_capital=initial_capital,
                final_capital=initial_capital,
                total_return=0,
                total_return_pct=0,
                total_trades=0,
                winning_trades=0,
                losing_trades=0,
                win_rate=0,
                max_drawdown=0,
                max_drawdown_pct=0,
                sharpe_ratio=0
            )
        
        capital = initial_capital
        position = 0  # 持仓股数
        trades = []
        equity_curve = []
        entry_price = 0
        
        peak_capital = initial_capital
        max_drawdown = 0
        
        for i in range(30, len(df)):
            current_data = df.iloc[:i+1]
            current_row = df.iloc[i]
            current_date = current_row.name if isinstance(current_row.name, datetime) else pd.to_datetime(current_row.name)
            current_price = current_row['close']
            
            # 获取策略信号
            signal = strategy_func(current_data)
            
            # 止损检查
            if position > 0 and entry_price > 0:
                loss_pct = (entry_price - current_price) / entry_price
                if loss_pct >= stop_loss:
                    # 止损卖出
                    sell_amount = position * current_price * (1 - commission_rate)
                    capital += sell_amount
                    
                    trades.append(Trade(
                        date=current_date,
                        action='SELL',
                        price=current_price,
                        shares=position,
                        amount=sell_amount,
                        reason='止损卖出'
                    ))
                    
                    position = 0
                    entry_price = 0
            
            # 执行交易信号
            if signal['signal'] == 'BUY' and position == 0:
                # 买入
                buy_amount = capital * position_size
                shares = int(buy_amount / current_price)
                
                if shares > 0:
                    cost = shares * current_price * (1 + commission_rate)
                    if cost <= capital:
                        capital -= cost
                        position = shares
                        entry_price = current_price
                        
                        trades.append(Trade(
                            date=current_date,
                            action='BUY',
                            price=current_price,
                            shares=shares,
                            amount=cost,
                            reason=signal.get('reason', '买入信号')
                        ))
            
            elif signal['signal'] == 'SELL' and position > 0:
                # 卖出
                sell_amount = position * current_price * (1 - commission_rate)
                capital += sell_amount
                
                trades.append(Trade(
                    date=current_date,
                    action='SELL',
                    price=current_price,
                    shares=position,
                    amount=sell_amount,
                    reason=signal.get('reason', '卖出信号')
                ))
                
                position = 0
                entry_price = 0
            
            # 计算当前权益
            current_equity = capital + position * current_price
            equity_curve.append({
                'date': current_date,
                'equity': current_equity,
                'price': current_price,
                'signal': signal['signal']
            })
            
            # 更新最大回撤
            if current_equity > peak_capital:
                peak_capital = current_equity
            drawdown = peak_capital - current_equity
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        
        # 最终清算
        final_capital = capital
        if position > 0:
            final_price = df.iloc[-1]['close']
            final_capital += position * final_price * (1 - commission_rate)
        
        # 计算统计指标
        total_return = final_capital - initial_capital
        total_return_pct = (total_return / initial_capital) * 100
        
        # 计算胜率
        completed_trades = []
        entry_trade = None
        for trade in trades:
            if trade.action == 'BUY':
                entry_trade = trade
            elif trade.action == 'SELL' and entry_trade is not None:
                completed_trades.append((entry_trade, trade))
                entry_trade = None
        
        winning_trades = 0
        losing_trades = 0
        for entry, exit in completed_trades:
            if exit.price > entry.price:
                winning_trades += 1
            else:
                losing_trades += 1
        
        total_completed = winning_trades + losing_trades
        win_rate = (winning_trades / total_completed * 100) if total_completed > 0 else 0
        
        # 计算夏普比率
        if len(equity_curve) > 1:
            returns = []
            for i in range(1, len(equity_curve)):
                daily_return = (equity_curve[i]['equity'] - equity_curve[i-1]['equity']) / equity_curve[i-1]['equity']
                returns.append(daily_return)
            
            returns = np.array(returns)
            if len(returns) > 0 and returns.std() > 0:
                sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(252)  # 年化
            else:
                sharpe_ratio = 0
        else:
            sharpe_ratio = 0
        
        max_drawdown_pct = (max_drawdown / initial_capital) * 100 if initial_capital > 0 else 0
        
        return BacktestResult(
            initial_capital=initial_capital,
            final_capital=final_capital,
            total_return=total_return,
            total_return_pct=total_return_pct,
            total_trades=len(completed_trades),
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            win_rate=win_rate,
            max_drawdown=max_drawdown,
            max_drawdown_pct=max_drawdown_pct,
            sharpe_ratio=sharpe_ratio,
            trades=trades,
            equity_curve=equity_curve
        )
    
    def compare_strategies(self, df: pd.DataFrame, strategies: Dict, 
                          initial_capital: float = 100000) -> Dict:
        """对比多个策略的回测结果"""
        results = {}
        
        for name, strategy_func in strategies.items():
            result = self.run_backtest(df, strategy_func, initial_capital)
            results[name] = {
                'total_return_pct': result.total_return_pct,
                'win_rate': result.win_rate,
                'max_drawdown_pct': result.max_drawdown_pct,
                'sharpe_ratio': result.sharpe_ratio,
                'total_trades': result.total_trades,
                'final_capital': result.final_capital
            }
        
        return results
    
    def monte_carlo_simulation(self, df: pd.DataFrame, strategy_func,
                               initial_capital: float = 100000,
                               runs: int = 100) -> Dict:
        """蒙特卡洛模拟"""
        returns = []
        max_drawdowns = []
        
        for _ in range(runs):
            # 随机打乱收益率（保持统计特性）
            returns_series = df['close'].pct_change().dropna()
            shuffled_returns = returns_series.sample(frac=1).reset_index(drop=True)
            
            # 重构价格序列
            prices = [df['close'].iloc[0]]
            for ret in shuffled_returns:
                prices.append(prices[-1] * (1 + ret))
            
            sim_df = pd.DataFrame({
                'close': prices,
                'high': prices,
                'low': prices,
                'open': prices
            })
            
            result = self.run_backtest(sim_df, strategy_func, initial_capital)
            returns.append(result.total_return_pct)
            max_drawdowns.append(result.max_drawdown_pct)
        
        returns = np.array(returns)
        max_drawdowns = np.array(max_drawdowns)
        
        return {
            'expected_return': returns.mean(),
            'return_std': returns.std(),
            'worst_case': np.percentile(returns, 5),
            'best_case': np.percentile(returns, 95),
            'expected_max_drawdown': max_drawdowns.mean(),
            'worst_drawdown': max_drawdowns.max(),
            'var_95': np.percentile(returns, 5)  # 95%置信度下的最大损失
        }

# 全局实例
backtest_service = BacktestService()
