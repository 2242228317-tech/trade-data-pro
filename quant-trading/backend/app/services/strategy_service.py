import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime
from .indicator_service import IndicatorService

class StrategyService:
    """量化策略服务"""
    
    def __init__(self):
        self.indicator = IndicatorService()
    
    def ma_cross_strategy(self, df: pd.DataFrame, short: int = 5, long: int = 20) -> Dict:
        """双均线交叉策略"""
        if len(df) < long + 5:
            return {'signal': 'HOLD', 'reason': 'Insufficient data'}
        
        df = df.copy()
        df['ma_short'] = self.indicator.ma(df['close'], short)
        df['ma_long'] = self.indicator.ma(df['close'], long)
        
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        # 金叉：短期均线上穿长期均线
        if latest['ma_short'] > latest['ma_long'] and prev['ma_short'] <= prev['ma_long']:
            return {
                'signal': 'BUY',
                'reason': f'MA{short}金叉MA{long}',
                'price': latest['close'],
                'strength': abs(latest['ma_short'] - latest['ma_long']) / latest['close'] * 100
            }
        
        # 死叉：短期均线下穿长期均线
        if latest['ma_short'] < latest['ma_long'] and prev['ma_short'] >= prev['ma_long']:
            return {
                'signal': 'SELL',
                'reason': f'MA{short}死叉MA{long}',
                'price': latest['close'],
                'strength': abs(latest['ma_short'] - latest['ma_long']) / latest['close'] * 100
            }
        
        return {
            'signal': 'HOLD',
            'reason': f'无交叉信号，MA{short}={latest["ma_short"]:.2f}, MA{long}={latest["ma_long"]:.2f}',
            'price': latest['close'],
            'strength': 0
        }
    
    def macd_strategy(self, df: pd.DataFrame) -> Dict:
        """MACD策略"""
        if len(df) < 30:
            return {'signal': 'HOLD', 'reason': 'Insufficient data'}
        
        df = df.copy()
        macd_data = self.indicator.macd(df['close'])
        df['diff'] = macd_data['diff']
        df['dea'] = macd_data['dea']
        df['macd'] = macd_data['macd']
        
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        # MACD金叉
        if latest['diff'] > latest['dea'] and prev['diff'] <= prev['dea']:
            if latest['macd'] > 0:
                return {
                    'signal': 'BUY',
                    'reason': 'MACD金叉(零轴上方，强势)',
                    'price': latest['close'],
                    'strength': abs(latest['macd'])
                }
            else:
                return {
                    'signal': 'BUY',
                    'reason': 'MACD金叉(零轴下方，弱势)',
                    'price': latest['close'],
                    'strength': abs(latest['macd']) * 0.5
                }
        
        # MACD死叉
        if latest['diff'] < latest['dea'] and prev['diff'] >= prev['dea']:
            if latest['macd'] < 0:
                return {
                    'signal': 'SELL',
                    'reason': 'MACD死叉(零轴下方，弱势)',
                    'price': latest['close'],
                    'strength': abs(latest['macd'])
                }
            else:
                return {
                    'signal': 'SELL',
                    'reason': 'MACD死叉(零轴上方，强势)',
                    'price': latest['close'],
                    'strength': abs(latest['macd']) * 0.5
                }
        
        return {
            'signal': 'HOLD',
            'reason': f'无MACD交叉信号',
            'price': latest['close'],
            'strength': 0
        }
    
    def kdj_strategy(self, df: pd.DataFrame) -> Dict:
        """KDJ策略"""
        if len(df) < 20:
            return {'signal': 'HOLD', 'reason': 'Insufficient data'}
        
        df = df.copy()
        kdj_data = self.indicator.kdj(df['high'], df['low'], df['close'])
        df['k'] = kdj_data['k']
        df['d'] = kdj_data['d']
        df['j'] = kdj_data['j']
        
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        # KDJ金叉且J值在合理区间
        if latest['k'] > latest['d'] and prev['k'] <= prev['d'] and latest['j'] < 80:
            return {
                'signal': 'BUY',
                'reason': f'KDJ金叉，J={latest["j"]:.2f}',
                'price': latest['close'],
                'strength': (80 - latest['j']) / 80 * 100
            }
        
        # KDJ死叉或J值超买
        if latest['k'] < latest['d'] and prev['k'] >= prev['d']:
            return {
                'signal': 'SELL',
                'reason': f'KDJ死叉，J={latest["j"]:.2f}',
                'price': latest['close'],
                'strength': min(latest['j'] / 100 * 100, 100)
            }
        
        if latest['j'] > 100:
            return {
                'signal': 'SELL',
                'reason': f'KDJ超买，J={latest["j"]:.2f}',
                'price': latest['close'],
                'strength': 80
            }
        
        return {
            'signal': 'HOLD',
            'reason': f'K={latest["k"]:.2f}, D={latest["d"]:.2f}, J={latest["j"]:.2f}',
            'price': latest['close'],
            'strength': 0
        }
    
    def boll_strategy(self, df: pd.DataFrame) -> Dict:
        """布林带策略"""
        if len(df) < 20:
            return {'signal': 'HOLD', 'reason': 'Insufficient data'}
        
        df = df.copy()
        boll_data = self.indicator.boll(df['close'])
        df['upper'] = boll_data['upper']
        df['mid'] = boll_data['mid']
        df['lower'] = boll_data['lower']
        
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        # 触及下轨反弹买入
        if latest['close'] > latest['lower'] and prev['close'] <= prev['lower']:
            return {
                'signal': 'BUY',
                'reason': '股价突破布林带下轨，反弹信号',
                'price': latest['close'],
                'strength': 70
            }
        
        # 触及上轨回落卖出
        if latest['close'] < latest['upper'] and prev['close'] >= prev['upper']:
            return {
                'signal': 'SELL',
                'reason': '股价跌破布林带上轨，回调信号',
                'price': latest['close'],
                'strength': 70
            }
        
        # 中轨支撑/压力
        if latest['close'] > latest['mid'] and prev['close'] <= prev['mid']:
            return {
                'signal': 'BUY',
                'reason': '股价突破布林带中轨',
                'price': latest['close'],
                'strength': 50
            }
        
        if latest['close'] < latest['mid'] and prev['close'] >= prev['mid']:
            return {
                'signal': 'SELL',
                'reason': '股价跌破布林带中轨',
                'price': latest['close'],
                'strength': 50
            }
        
        return {
            'signal': 'HOLD',
            'reason': f'价格在布林带{latest["lower"]:.2f}-{latest["upper"]:.2f}区间内运行',
            'price': latest['close'],
            'strength': 0
        }
    
    def rsi_strategy(self, df: pd.DataFrame) -> Dict:
        """RSI策略"""
        if len(df) < 20:
            return {'signal': 'HOLD', 'reason': 'Insufficient data'}
        
        df = df.copy()
        rsi_data = self.indicator.rsi(df['close'])
        df['rsi6'] = rsi_data['rsi1']
        
        latest = df.iloc[-1]
        
        # RSI超卖买入
        if latest['rsi6'] < 20:
            return {
                'signal': 'BUY',
                'reason': f'RSI超卖({latest["rsi6"]:.2f})，反弹概率大',
                'price': latest['close'],
                'strength': (20 - latest['rsi6']) / 20 * 100
            }
        
        # RSI超买卖出
        if latest['rsi6'] > 80:
            return {
                'signal': 'SELL',
                'reason': f'RSI超买({latest["rsi6"]:.2f})，回调概率大',
                'price': latest['close'],
                'strength': (latest['rsi6'] - 80) / 20 * 100
            }
        
        return {
            'signal': 'HOLD',
            'reason': f'RSI={latest["rsi6"]:.2f}，处于正常区间',
            'price': latest['close'],
            'strength': 0
        }
    
    def combined_strategy(self, df: pd.DataFrame) -> Dict:
        """综合策略：多指标共振"""
        if len(df) < 30:
            return {'signal': 'HOLD', 'reason': 'Insufficient data'}
        
        signals = []
        
        # 收集各策略信号
        ma_signal = self.ma_cross_strategy(df)
        macd_signal = self.macd_strategy(df)
        kdj_signal = self.kdj_strategy(df)
        rsi_signal = self.rsi_strategy(df)
        
        signals.extend([ma_signal, macd_signal, kdj_signal, rsi_signal])
        
        # 统计买入/卖出信号数量
        buy_count = sum(1 for s in signals if s['signal'] == 'BUY')
        sell_count = sum(1 for s in signals if s['signal'] == 'SELL')
        
        latest = df.iloc[-1]
        
        # 多数指标共振才给出信号
        if buy_count >= 3:
            return {
                'signal': 'BUY',
                'reason': f'多指标共振买入({buy_count}/4个指标发出买入信号)',
                'price': latest['close'],
                'strength': buy_count / 4 * 100,
                'details': {
                    'MA': ma_signal,
                    'MACD': macd_signal,
                    'KDJ': kdj_signal,
                    'RSI': rsi_signal
                }
            }
        
        if sell_count >= 3:
            return {
                'signal': 'SELL',
                'reason': f'多指标共振卖出({sell_count}/4个指标发出卖出信号)',
                'price': latest['close'],
                'strength': sell_count / 4 * 100,
                'details': {
                    'MA': ma_signal,
                    'MACD': macd_signal,
                    'KDJ': kdj_signal,
                    'RSI': rsi_signal
                }
            }
        
        # 部分指标信号
        if buy_count >= 2:
            return {
                'signal': 'WEAK_BUY',
                'reason': f'部分指标支持买入({buy_count}/4)',
                'price': latest['close'],
                'strength': buy_count / 4 * 100
            }
        
        if sell_count >= 2:
            return {
                'signal': 'WEAK_SELL',
                'reason': f'部分指标支持卖出({sell_count}/4)',
                'price': latest['close'],
                'strength': sell_count / 4 * 100
            }
        
        return {
            'signal': 'HOLD',
            'reason': f'指标信号分歧，建议观望(买:{buy_count}, 卖:{sell_count})',
            'price': latest['close'],
            'strength': 0
        }
    
    def run_strategy(self, df: pd.DataFrame, strategy_type: str = 'combined') -> Dict:
        """运行指定策略"""
        strategies = {
            'ma_cross': self.ma_cross_strategy,
            'macd': self.macd_strategy,
            'kdj': self.kdj_strategy,
            'boll': self.boll_strategy,
            'rsi': self.rsi_strategy,
            'combined': self.combined_strategy
        }
        
        if strategy_type not in strategies:
            return {'signal': 'ERROR', 'reason': f'Unknown strategy: {strategy_type}'}
        
        return strategies[strategy_type](df)

# 全局实例
strategy_service = StrategyService()
