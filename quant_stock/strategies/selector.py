"""
选股策略模块
包含多种选股策略实现
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
from data.data_fetcher import DataFetcher
from indicators.technical import TechnicalIndicators


class StockSelector:
    """选股策略基类"""
    
    def __init__(self, fetcher: DataFetcher = None):
        self.fetcher = fetcher or DataFetcher()
    
    def select(self, stock_codes: List[str], **kwargs) -> pd.DataFrame:
        """
        选股接口
        
        Args:
            stock_codes: 股票代码列表
            
        Returns:
            选中的股票及评分
        """
        raise NotImplementedError


class BreakoutSelector(StockSelector):
    """突破策略选股器"""
    
    def select(self, stock_codes: List[str] = None, 
               min_volume_ratio: float = 1.5,
               min_price_change: float = 3.0,
               top_n: int = 10) -> pd.DataFrame:
        """
        突破策略选股
        
        条件:
        1. 今日涨幅 > min_price_change%
        2. 成交量放大 > min_volume_ratio 倍
        3. 价格突破 20 日高点
        4. 均线多头排列
        
        Args:
            stock_codes: 股票池，None 表示全市场
            min_volume_ratio: 最小成交量放大倍数
            min_price_change: 最小涨幅百分比
            top_n: 返回前 N 只股票
            
        Returns:
            选中的股票列表及信号强度
        """
        if stock_codes is None:
            # Get all market stocks
            stock_list = self.fetcher.get_stock_list()
            # Filter out suspended stocks
            if 'price' in stock_list.columns:
                stock_list = stock_list[stock_list['price'] > 0]
                stock_codes = stock_list['code'].head(100).tolist()
            elif '最新价' in stock_list.columns:
                stock_list = stock_list[
                    (stock_list['最新价'] > 0) & 
                    (stock_list['涨跌幅'].notna())
                ]
                stock_codes = stock_list['代码'].head(100).tolist()
            else:
                stock_codes = []
        
        results = []
        
        for code in stock_codes:
            try:
                df = self.fetcher.get_daily_data(code)
                if len(df) < 30:
                    continue
                
                # 计算指标
                df = TechnicalIndicators.calculate_all(df)
                latest = df.iloc[-1]
                prev = df.iloc[-2] if len(df) > 1 else latest
                
                # Check breakout conditions
                score = 0
                signals = []
                
                # 1. Price change condition
                pct_change = latest.get('pct_change', 0)
                if pct_change >= min_price_change:
                    score += 2
                    signals.append(f"Change:{pct_change:.2f}%")
                
                # 2. Volume expansion
                if latest.get('volume', 0) > 0 and prev.get('volume', 0) > 0:
                    vol_ratio = latest['volume'] / prev['volume']
                    if vol_ratio >= min_volume_ratio:
                        score += 2
                        signals.append(f"VolRatio:{vol_ratio:.2f}")
                
                # 3. Break 20-day high
                high_20 = df['high'].iloc[-21:-1].max() if len(df) > 20 else latest['high']
                if latest['close'] > high_20:
                    score += 3
                    signals.append("Break20High")
                
                # 4. Bullish MA alignment
                if (latest.get('MA5', 0) > latest.get('MA10', 0) and 
                    latest.get('MA10', 0) > latest.get('MA20', 0) and
                    latest.get('MA20', 0) > latest.get('MA60', 0)):
                    score += 2
                    signals.append("BullishMA")
                
                # 5. MACD golden cross
                if (latest.get('DIF', 0) > latest.get('DEA', 0) and 
                    prev.get('DIF', 0) <= prev.get('DEA', 0)):
                    score += 2
                    signals.append("MACD_Golden")
                
                # 6. KDJ golden cross
                if (latest.get('K', 0) > latest.get('D', 0) and 
                    prev.get('K', 0) <= prev.get('D', 0)):
                    score += 1
                    signals.append("KDJ_Golden")
                
                if score >= 5:  # At least 3 conditions met
                    results.append({
                        'code': code,
                        'name': f'Stock_{code}',
                        'price': round(latest['close'], 2),
                        'change': round(pct_change, 2),
                        'score': score,
                        'signals': ' | '.join(signals),
                        'advice': self._generate_advice(latest, df)
                    })
                
            except Exception as e:
                continue
        
        if not results:
            return pd.DataFrame()
        
        result_df = pd.DataFrame(results)
        result_df = result_df.sort_values('score', ascending=False).head(top_n)
        return result_df
    
    def _generate_advice(self, latest: pd.Series, df: pd.DataFrame) -> str:
        """Generate trading advice"""
        advice = []
        
        # Support level
        support = df['low'].iloc[-10:].min()
        advice.append(f"Support:{support:.2f}")
        
        # Resistance level
        resistance = df['high'].iloc[-20:].max()
        advice.append(f"Resist:{resistance:.2f}")
        
        # Stop loss
        stop_loss = latest['close'] * 0.95
        advice.append(f"Stop:{stop_loss:.2f}")
        
        return ' | '.join(advice)


class ValueSelector(StockSelector):
    """Value strategy (Low valuation + Fundamentals)"""
    
    def select(self, stock_codes: List[str] = None,
               max_pe: float = 20,
               min_roe: float = 10,
               top_n: int = 10) -> pd.DataFrame:
        """
        Value stock selection
        
        Conditions:
        1. PE < max_pe
        2. ROE > min_roe%
        3. Price above yearly MA
        
        Args:
            stock_codes: Stock pool
            max_pe: Max PE ratio
            min_roe: Min ROE
            top_n: Number to return
            
        Returns:
            Selected stocks
        """
        # Simplified implementation - requires financial data
        print("Value strategy requires financial data, use professional data source")
        return pd.DataFrame()


class TrendSelector(StockSelector):
    """Trend following strategy"""
    
    def select(self, stock_codes: List[str] = None,
               min_ma_slope: float = 0.02,
               top_n: int = 10) -> pd.DataFrame:
        """
        Trend following stock selection
        
        Conditions:
        1. 20-day MA slope upward
        2. Price above MA
        3. Volume expanding
        
        Args:
            stock_codes: Stock pool
            min_ma_slope: Min MA slope
            top_n: Number to return
            
        Returns:
            Selected stocks
        """
        if stock_codes is None:
            stock_list = self.fetcher.get_stock_list()
            if 'code' in stock_list.columns:
                stock_codes = stock_list['code'].head(100).tolist()
            elif '代码' in stock_list.columns:
                stock_codes = stock_list['代码'].head(100).tolist()
            else:
                stock_codes = []
        
        results = []
        
        for code in stock_codes:
            try:
                df = self.fetcher.get_daily_data(code)
                if len(df) < 60:
                    continue
                
                df = TechnicalIndicators.calculate_all(df)
                latest = df.iloc[-1]
                
                score = 0
                signals = []
                
                # Calculate 20-day MA slope
                ma20_recent = df['MA20'].iloc[-10:].values
                if len(ma20_recent) >= 10:
                    slope = (ma20_recent[-1] - ma20_recent[0]) / ma20_recent[0]
                    if slope > min_ma_slope:
                        score += 3
                        signals.append(f"均线斜率{slope*100:.2f}%")
                
                # 股价在 MA20 上方
                if latest['close'] > latest.get('MA20', 0):
                    score += 2
                    signals.append("股价站上 20 日线")
                
                # 成交量趋势
                vol_ma5 = df['VOL_MA5'].iloc[-1]
                vol_ma10 = df['VOL_MA10'].iloc[-1]
                if vol_ma5 > vol_ma10:
                    score += 1
                    signals.append("成交量放大")
                
                if score >= 4:
                    results.append({
                        '代码': code,
                        '名称': '',
                        '价格': round(latest['close'], 2),
                        '得分': score,
                        '信号': ' | '.join(signals)
                    })
                
            except Exception as e:
                continue
        
        if not results:
            return pd.DataFrame()
        
        result_df = pd.DataFrame(results)
        result_df = result_df.sort_values('得分', ascending=False).head(top_n)
        return result_df


# 策略工厂
def get_selector(strategy_name: str) -> StockSelector:
    """
    获取选股器实例
    
    Args:
        strategy_name: 策略名称
        
    Returns:
        选股器实例
    """
    selectors = {
        'breakout': BreakoutSelector,
        'value': ValueSelector,
        'trend': TrendSelector
    }
    
    selector_class = selectors.get(strategy_name.lower(), BreakoutSelector)
    return selector_class()


# 测试
if __name__ == "__main__":
    selector = BreakoutSelector()
    
    print("执行突破策略选股...")
    result = selector.select(top_n=5)
    
    if len(result) > 0:
        print("\n选股结果:")
        print(result.to_string(index=False))
    else:
        print("未找到符合条件的股票")
