"""
技术指标计算模块
包含常用的技术分析指标
"""

import pandas as pd
import numpy as np
from typing import Tuple, Optional


class TechnicalIndicators:
    """技术指标计算器"""
    
    @staticmethod
    def MA(df: pd.DataFrame, periods: list = [5, 10, 20, 60]) -> pd.DataFrame:
        """
        计算移动平均线
        
        Args:
            df: 包含 close 列的 DataFrame
            periods: 周期列表
            
        Returns:
            添加 MA 列的 DataFrame
        """
        df = df.copy()
        for period in periods:
            df[f'MA{period}'] = df['close'].rolling(window=period).mean()
        return df
    
    @staticmethod
    def EMA(df: pd.DataFrame, periods: list = [12, 26]) -> pd.DataFrame:
        """
        计算指数移动平均线
        
        Args:
            df: 包含 close 列的 DataFrame
            periods: 周期列表
            
        Returns:
            添加 EMA 列的 DataFrame
        """
        df = df.copy()
        for period in periods:
            df[f'EMA{period}'] = df['close'].ewm(span=period, adjust=False).mean()
        return df
    
    @staticmethod
    def MACD(df: pd.DataFrame, fast: int = 12, slow: int = 26, 
             signal: int = 9) -> pd.DataFrame:
        """
        计算 MACD 指标
        
        Args:
            df: 包含 close 列的 DataFrame
            fast: 快线周期
            slow: 慢线周期
            signal: 信号线周期
            
        Returns:
            添加 MACD/DIF/DEA 列的 DataFrame
        """
        df = df.copy()
        
        # 计算 DIF（快线 - 慢线）
        ema_fast = df['close'].ewm(span=fast, adjust=False).mean()
        ema_slow = df['close'].ewm(span=slow, adjust=False).mean()
        df['DIF'] = ema_fast - ema_slow
        
        # 计算 DEA（DIF 的 EMA）
        df['DEA'] = df['DIF'].ewm(span=signal, adjust=False).mean()
        
        # 计算 MACD 柱
        df['MACD'] = (df['DIF'] - df['DEA']) * 2
        
        return df
    
    @staticmethod
    def KDJ(df: pd.DataFrame, n: int = 9, m1: int = 3, m2: int = 3) -> pd.DataFrame:
        """
        计算 KDJ 指标
        
        Args:
            df: 包含 high/low/close 列的 DataFrame
            n: RSV 周期
            m1: K 值周期
            m2: D 值周期
            
        Returns:
            添加 K/D/J 列的 DataFrame
        """
        df = df.copy()
        
        # 计算 RSV
        lowest_low = df['low'].rolling(window=n).min()
        highest_high = df['high'].rolling(window=n).max()
        df['RSV'] = (df['close'] - lowest_low) / (highest_high - lowest_low) * 100
        
        # 计算 K 值
        df['K'] = df['RSV'].ewm(com=m1-1, adjust=False).mean()
        
        # 计算 D 值
        df['D'] = df['K'].ewm(com=m2-1, adjust=False).mean()
        
        # 计算 J 值
        df['J'] = 3 * df['K'] - 2 * df['D']
        
        return df
    
    @staticmethod
    def RSI(df: pd.DataFrame, periods: list = [6, 12, 24]) -> pd.DataFrame:
        """
        计算 RSI 指标
        
        Args:
            df: 包含 close 列的 DataFrame
            periods: 周期列表
            
        Returns:
            添加 RSI 列的 DataFrame
        """
        df = df.copy()
        
        for period in periods:
            delta = df['close'].diff()
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            
            avg_gain = gain.rolling(window=period).mean()
            avg_loss = loss.rolling(window=period).mean()
            
            rs = avg_gain / avg_loss
            df[f'RSI{period}'] = 100 - (100 / (1 + rs))
        
        return df
    
    @staticmethod
    def BOLL(df: pd.DataFrame, period: int = 20, 
             width: float = 2.0) -> pd.DataFrame:
        """
        计算布林带
        
        Args:
            df: 包含 close 列的 DataFrame
            period: 周期
            width: 标准差倍数
            
        Returns:
            添加 BOLL 上中下轨的 DataFrame
        """
        df = df.copy()
        
        # 中轨
        df['BOLL_MID'] = df['close'].rolling(window=period).mean()
        
        # 标准差
        std = df['close'].rolling(window=period).std()
        
        # 上轨
        df['BOLL_UPPER'] = df['BOLL_MID'] + width * std
        
        # 下轨
        df['BOLL_LOWER'] = df['BOLL_MID'] - width * std
        
        return df
    
    @staticmethod
    def VOL_MA(df: pd.DataFrame, periods: list = [5, 10]) -> pd.DataFrame:
        """
        计算成交量均线
        
        Args:
            df: 包含 volume 列的 DataFrame
            periods: 周期列表
            
        Returns:
            添加成交量均线列的 DataFrame
        """
        df = df.copy()
        for period in periods:
            df[f'VOL_MA{period}'] = df['volume'].rolling(window=period).mean()
        return df
    
    @staticmethod
    def ATR(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """
        计算 ATR（平均真实波幅）
        
        Args:
            df: 包含 high/low/close 列的 DataFrame
            period: 周期
            
        Returns:
            添加 ATR 列的 DataFrame
        """
        df = df.copy()
        
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())
        
        tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        df['ATR'] = tr.rolling(window=period).mean()
        
        return df
    
    @staticmethod
    def calculate_all(df: pd.DataFrame) -> pd.DataFrame:
        """
        一次性计算所有常用指标
        
        Args:
            df: 包含 OHLCV 数据的 DataFrame
            
        Returns:
            添加所有技术指标的 DataFrame
        """
        df = df.copy()
        
        # 均线
        df = TechnicalIndicators.MA(df, [5, 10, 20, 60])
        
        # MACD
        df = TechnicalIndicators.MACD(df)
        
        # KDJ
        df = TechnicalIndicators.KDJ(df)
        
        # RSI
        df = TechnicalIndicators.RSI(df, [6, 12, 24])
        
        # 布林带
        df = TechnicalIndicators.BOLL(df)
        
        # 成交量均线
        df = TechnicalIndicators.VOL_MA(df, [5, 10])
        
        # ATR
        df = TechnicalIndicators.ATR(df)
        
        return df


# 测试代码
if __name__ == "__main__":
    from data.data_fetcher import DataFetcher
    
    fetcher = DataFetcher()
    df = fetcher.get_daily_data("000001")
    
    if len(df) > 0:
        print("原始数据:")
        print(df.tail())
        
        df = TechnicalIndicators.calculate_all(df)
        
        print("\n添加指标后:")
        print(df.tail())
        
        # 检查 NaN 值
        print(f"\nNaN 值统计:")
        print(df.isna().sum())
