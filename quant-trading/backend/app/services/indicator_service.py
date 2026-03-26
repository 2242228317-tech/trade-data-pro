import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional

class IndicatorService:
    """技术指标计算服务"""
    
    @staticmethod
    def ma(close: pd.Series, period: int) -> pd.Series:
        """简单移动平均线"""
        return close.rolling(window=period).mean()
    
    @staticmethod
    def ema(close: pd.Series, period: int) -> pd.Series:
        """指数移动平均线"""
        return close.ewm(span=period, adjust=False).mean()
    
    @staticmethod
    def macd(close: pd.Series, short: int = 12, long: int = 26, signal: int = 9) -> Dict:
        """MACD指标"""
        ema_short = IndicatorService.ema(close, short)
        ema_long = IndicatorService.ema(close, long)
        diff = ema_short - ema_long
        dea = IndicatorService.ema(diff, signal)
        macd_val = (diff - dea) * 2
        
        return {
            'diff': diff,
            'dea': dea,
            'macd': macd_val
        }
    
    @staticmethod
    def kdj(high: pd.Series, low: pd.Series, close: pd.Series, 
            n: int = 9, m1: int = 3, m2: int = 3) -> Dict:
        """KDJ随机指标"""
        rsv = (close - low.rolling(window=n).min()) / (high.rolling(window=n).max() - low.rolling(window=n).min()) * 100
        k = rsv.ewm(com=m1-1, adjust=False).mean()
        d = k.ewm(com=m2-1, adjust=False).mean()
        j = k * 3 - d * 2
        
        return {
            'k': k,
            'd': d,
            'j': j
        }
    
    @staticmethod
    def boll(close: pd.Series, n: int = 20, p: float = 2.0) -> Dict:
        """布林带"""
        mid = IndicatorService.ma(close, n)
        std = close.rolling(window=n).std()
        upper = mid + std * p
        lower = mid - std * p
        
        return {
            'upper': upper,
            'mid': mid,
            'lower': lower
        }
    
    @staticmethod
    def rsi(close: pd.Series, n1: int = 6, n2: int = 12, n3: int = 24) -> Dict:
        """RSI相对强弱指标"""
        diff = close.diff()
        
        def calc_rsi(n):
            gain = diff.where(diff > 0, 0).rolling(window=n).mean()
            loss = (-diff.where(diff < 0, 0)).rolling(window=n).mean()
            rs = gain / loss
            return 100 - (100 / (1 + rs))
        
        return {
            'rsi1': calc_rsi(n1),
            'rsi2': calc_rsi(n2),
            'rsi3': calc_rsi(n3)
        }
    
    @staticmethod
    def dmi(high: pd.Series, low: pd.Series, close: pd.Series, 
            m1: int = 14, m2: int = 6) -> Dict:
        """DMI趋向指标"""
        tr1 = high - low
        tr2 = abs(high - close.shift(1))
        tr3 = abs(low - close.shift(1))
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        
        hd = high - high.shift(1)
        ld = low.shift(1) - low
        
        dmp = np.where((hd > 0) & (hd > ld), hd, 0)
        dmm = np.where((ld > 0) & (ld > hd), ld, 0)
        
        dmp = pd.Series(dmp, index=high.index).rolling(window=m1).sum()
        dmm = pd.Series(dmm, index=high.index).rolling(window=m1).sum()
        tr_sum = tr.rolling(window=m1).sum()
        
        di1 = dmp * 100 / tr_sum
        di2 = dmm * 100 / tr_sum
        adx = abs(di2 - di1) / (di1 + di2) * 100
        adx = adx.rolling(window=m2).mean()
        adxr = (adx + adx.shift(m2)) / 2
        
        return {
            'di1': di1,
            'di2': di2,
            'adx': adx,
            'adxr': adxr
        }
    
    @staticmethod
    def wr(high: pd.Series, low: pd.Series, close: pd.Series, 
           n: int = 10, n1: int = 6) -> Dict:
        """W&R威廉指标"""
        wr1 = (high.rolling(window=n).max() - close) / (high.rolling(window=n).max() - low.rolling(window=n).min()) * 100
        wr2 = (high.rolling(window=n1).max() - close) / (high.rolling(window=n1).max() - low.rolling(window=n1).min()) * 100
        
        return {
            'wr1': wr1,
            'wr2': wr2
        }
    
    @staticmethod
    def bias(close: pd.Series, l1: int = 5, l4: int = 3, l5: int = 10) -> Dict:
        """BIAS乖离率"""
        ma5 = IndicatorService.ma(close, l1)
        ma3 = IndicatorService.ma(close, l4)
        ma10 = IndicatorService.ma(close, l5)
        
        return {
            'bias': (close - ma5) / ma5 * 100,
            'bias2': (close - ma3) / ma3 * 100,
            'bias3': (close - ma10) / ma10 * 100
        }
    
    @staticmethod
    def atr(high: pd.Series, low: pd.Series, close: pd.Series, n: int = 14) -> pd.Series:
        """ATR平均真实波幅"""
        tr1 = high - low
        tr2 = abs(high - close.shift(1))
        tr3 = abs(low - close.shift(1))
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        return tr.rolling(window=n).mean()
    
    @staticmethod
    def calculate_all(df: pd.DataFrame) -> pd.DataFrame:
        """计算所有技术指标"""
        if df.empty or len(df) < 60:
            return df
        
        close = df['close']
        high = df['high']
        low = df['low']
        
        # 移动平均线
        df['ma5'] = IndicatorService.ma(close, 5)
        df['ma10'] = IndicatorService.ma(close, 10)
        df['ma20'] = IndicatorService.ma(close, 20)
        df['ma30'] = IndicatorService.ma(close, 30)
        df['ma60'] = IndicatorService.ma(close, 60)
        
        # MACD
        macd_data = IndicatorService.macd(close)
        df['macd_diff'] = macd_data['diff']
        df['macd_dea'] = macd_data['dea']
        df['macd'] = macd_data['macd']
        
        # KDJ
        kdj_data = IndicatorService.kdj(high, low, close)
        df['kdj_k'] = kdj_data['k']
        df['kdj_d'] = kdj_data['d']
        df['kdj_j'] = kdj_data['j']
        
        # BOLL
        boll_data = IndicatorService.boll(close)
        df['boll_upper'] = boll_data['upper']
        df['boll_mid'] = boll_data['mid']
        df['boll_lower'] = boll_data['lower']
        
        # RSI
        rsi_data = IndicatorService.rsi(close)
        df['rsi6'] = rsi_data['rsi1']
        df['rsi12'] = rsi_data['rsi2']
        df['rsi24'] = rsi_data['rsi3']
        
        # DMI
        dmi_data = IndicatorService.dmi(high, low, close)
        df['dmi_di1'] = dmi_data['di1']
        df['dmi_di2'] = dmi_data['di2']
        df['dmi_adx'] = dmi_data['adx']
        
        # 涨跌幅度
        df['change_pct'] = close.pct_change() * 100
        
        return df
    
    @staticmethod
    def get_latest_signals(df: pd.DataFrame) -> Dict:
        """获取最新技术指标信号"""
        if df.empty or len(df) < 2:
            return {}
        
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        signals = {
            # MA信号
            'ma_trend': 'UP' if latest['ma5'] > latest['ma10'] else 'DOWN',
            'ma_golden_cross': latest['ma5'] > latest['ma10'] and prev['ma5'] <= prev['ma10'],
            'ma_death_cross': latest['ma5'] < latest['ma10'] and prev['ma5'] >= prev['ma10'],
            
            # MACD信号
            'macd_golden_cross': latest['macd_diff'] > latest['macd_dea'] and prev['macd_diff'] <= prev['macd_dea'],
            'macd_death_cross': latest['macd_diff'] < latest['macd_dea'] and prev['macd_diff'] >= prev['macd_dea'],
            'macd_positive': latest['macd'] > 0,
            
            # KDJ信号
            'kdj_overbought': latest['kdj_j'] > 80,
            'kdj_oversold': latest['kdj_j'] < 20,
            'kdj_golden_cross': latest['kdj_k'] > latest['kdj_d'] and prev['kdj_k'] <= prev['kdj_d'],
            
            # BOLL信号
            'boll_position': 'UPPER' if latest['close'] > latest['boll_mid'] else 'LOWER',
            'boll_break_upper': latest['close'] > latest['boll_upper'],
            'boll_break_lower': latest['close'] < latest['boll_lower'],
            
            # RSI信号
            'rsi_overbought': latest['rsi6'] > 80,
            'rsi_oversold': latest['rsi6'] < 20,
        }
        
        return signals

# 全局实例
indicator_service = IndicatorService()
