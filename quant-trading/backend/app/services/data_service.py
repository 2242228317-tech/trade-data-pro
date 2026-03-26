import tushare as ts
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json
import os

# Tushare API Token - 用户可以替换为自己的token
TS_TOKEN = "b31e0ac207a5a45e0f7503aff25bf6bd929b88fe1d017a034ee0d530"

try:
    ts.set_token(TS_TOKEN)
    pro = ts.pro_api()
except:
    pro = None

class DataService:
    def __init__(self):
        self.pro = pro
        
    def get_daily_data(self, code: str, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """获取股票日线数据"""
        if end_date is None:
            end_date = datetime.now().strftime('%Y%m%d')
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
        
        # 转换股票代码格式
        ts_code = self._convert_code(code)
        
        try:
            df = self.pro.daily(ts_code=ts_code, start_date=start_date, end_date=end_date)
            if df is not None and not df.empty:
                df = df.sort_values('trade_date')
                df['trade_date'] = pd.to_datetime(df['trade_date'])
                df.set_index('trade_date', inplace=True)
            return df
        except Exception as e:
            print(f"Error fetching data for {code}: {e}")
            return pd.DataFrame()
    
    def get_realtime_data(self) -> pd.DataFrame:
        """获取当日所有股票实时行情"""
        try:
            df = ts.get_today_all()
            if df is not None and not df.empty:
                # 过滤ST股票
                df = df[~df.name.str.contains('ST', na=False)]
                # 计算流通市值
                df['liutongliang'] = df['nmc'] / df['trade']
                df['amount_yi'] = round(df['amount'] / 100000000, 2)
            return df
        except Exception as e:
            print(f"Error fetching realtime data: {e}")
            return pd.DataFrame()
    
    def get_stock_basic(self) -> pd.DataFrame:
        """获取股票基础信息"""
        try:
            df = self.pro.stock_basic(exchange='', list_status='L', 
                                     fields='ts_code,symbol,name,area,industry,list_date')
            return df
        except Exception as e:
            print(f"Error fetching stock basic: {e}")
            return pd.DataFrame()
    
    def get_money_flow(self, code: str) -> Dict:
        """获取资金流向数据"""
        try:
            ts_code = self._convert_code(code)
            df = self.pro.moneyflow(ts_code=ts_code)
            if df is not None and not df.empty:
                latest = df.iloc[0]
                return {
                    'buy_elg_amount': latest.get('buy_elg_amount', 0),  # 超大单买入
                    'sell_elg_amount': latest.get('sell_elg_amount', 0),  # 超大单卖出
                    'net_mf_amount': latest.get('net_mf_amount', 0),  # 净流入
                }
            return {}
        except Exception as e:
            print(f"Error fetching money flow: {e}")
            return {}
    
    def filter_stocks(self, min_volume: float = 15000000, min_amount: float = 1, 
                     min_turnover: float = 3) -> pd.DataFrame:
        """筛选股票：排除ST、成交量>1500万、成交额>1亿、换手率>3%"""
        df = self.get_realtime_data()
        if df.empty:
            return df
        
        # 应用筛选条件
        df = df[df["volume"] > min_volume]
        df = df[df["amount_yi"] > min_amount]
        df = df[df["turnoverratio"] > min_turnover]
        df = df.sort_values(by="turnoverratio", ascending=False)
        
        return df
    
    def _convert_code(self, code: str) -> str:
        """转换股票代码格式为tushare格式"""
        code = code.replace('.XSHG', '').replace('.XSHE', '')
        if code.startswith('6'):
            return f"{code}.SH"
        else:
            return f"{code}.SZ"
    
    def get_index_data(self, index_code: str = '000001.SH', 
                      start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """获取指数数据"""
        if end_date is None:
            end_date = datetime.now().strftime('%Y%m%d')
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
        
        try:
            df = self.pro.index_daily(ts_code=index_code, start_date=start_date, end_date=end_date)
            if df is not None and not df.empty:
                df = df.sort_values('trade_date')
                df['trade_date'] = pd.to_datetime(df['trade_date'])
                df.set_index('trade_date', inplace=True)
            return df
        except Exception as e:
            print(f"Error fetching index data: {e}")
            return pd.DataFrame()

# 全局数据服务实例
data_service = DataService()
