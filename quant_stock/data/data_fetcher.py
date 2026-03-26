"""
A-Stock Data Fetcher Module
Supports akshare and mock data sources
"""

import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Optional, Dict
import time


class DataFetcher:
    """A-Stock Data Fetcher"""
    
    def __init__(self, source: str = "akshare"):
        """
        Initialize data fetcher
        
        Args:
            source: Data source, supports 'akshare' or 'mock'
        """
        self.source = source
        self.cache = {}
        self.use_mock = False
        
    def get_stock_list(self, market: str = "A") -> pd.DataFrame:
        """
        Get stock list
        
        Args:
            market: Market type, 'A' for A-shares
            
        Returns:
            DataFrame with stock codes and names
        """
        if self.use_mock:
            from .mock_data import get_mock_stock_list
            return get_mock_stock_list()
            
        try:
            # Get A-share real-time quote list
            df = ak.stock_zh_a_spot_em()
            return df[['代码', '名称', '最新价', '涨跌幅', '成交量', '成交额']]
        except Exception as e:
            print(f"[Error] Failed to fetch stock list: {e}")
            print("[Info] Switching to demo mode...")
            self.use_mock = True
            from .mock_data import get_mock_stock_list
            return get_mock_stock_list()
    
    def get_daily_data(self, stock_code: str, start_date: str = None, 
                       end_date: str = None, adjust: str = "qfq") -> pd.DataFrame:
        """
        Get daily data - tries baostock first, then akshare, then mock
        """
        if end_date is None:
            end_date = datetime.now().strftime("%Y%m%d")
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y%m%d")
        
        cache_key = f"{stock_code}_{start_date}_{end_date}_{adjust}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # Try baostock first (works with mobile hotspot)
        try:
            import baostock as bs
            bs.login()
            
            # Format code for baostock (add .sz or .sh)
            if stock_code.startswith('6'):
                bs_code = f"{stock_code}.sh"
            else:
                bs_code = f"{stock_code}.sz"
            
            rs = bs.query_history_k_data_plus(
                bs_code,
                "date,open,high,low,close,volume",
                start_date=start_date,
                end_date=end_date,
                frequency="d",
                adjustflag="3"  # 3 for post-adjusted
            )
            
            data_list = []
            while (rs.error_code == '0') and rs.next():
                data_list.append(rs.get_row_data())
            
            bs.logout()
            
            if len(data_list) > 0:
                df = pd.DataFrame(data_list, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
                df['date'] = pd.to_datetime(df['date'])
                df['open'] = df['open'].astype(float)
                df['high'] = df['high'].astype(float)
                df['low'] = df['low'].astype(float)
                df['close'] = df['close'].astype(float)
                df['volume'] = df['volume'].astype(float)
                df['amount'] = df['volume'] * df['close']
                df['pct_change'] = df['close'].pct_change() * 100
                df['change'] = df['close'].diff()
                df = df.sort_values('date').reset_index(drop=True)
                
                self.cache[cache_key] = df
                print(f"[Info] Got real data from baostock for {stock_code}")
                return df
            
        except Exception as e:
            print(f"[Info] Baostock failed: {e}, trying akshare...")
        
        # Fall back to akshare
        try:
            df = ak.stock_zh_a_hist(
                symbol=stock_code,
                period="daily",
                start_date=start_date,
                end_date=end_date,
                adjust=adjust
            )
            
            df = df.rename(columns={
                '日期': 'date', '开盘': 'open', '收盘': 'close',
                '最高': 'high', '最低': 'low', '成交量': 'volume',
                '成交额': 'amount', '振幅': 'amplitude',
                '涨跌幅': 'pct_change', '涨跌额': 'change'
            })
            
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date').reset_index(drop=True)
            
            self.cache[cache_key] = df
            print(f"[Info] Got real data from akshare for {stock_code}")
            return df
            
        except Exception as e:
            print(f"[Error] Failed to fetch real data for {stock_code}: {e}")
            print("[Info] Switching to demo mode with mock data...")
            self.use_mock = True
            from .mock_data import generate_mock_daily_data
            return generate_mock_daily_data(stock_code)
    
    def get_minute_data(self, stock_code: str, period: str = "60") -> pd.DataFrame:
        """
        Get minute data
        
        Args:
            stock_code: Stock code
            period: Period, '1', '5', '15', '30', '60' minutes
            
        Returns:
            Minute data DataFrame
        """
        try:
            period_map = {
                '1': '1',
                '5': '5',
                '15': '15',
                '30': '30',
                '60': '60'
            }
            
            df = ak.stock_zh_a_hist_min_em(
                symbol=stock_code,
                period=period_map.get(period, '60'),
                adjust="qfq"
            )
            
            df = df.rename(columns={
                '时间': 'datetime',
                '开盘': 'open',
                '收盘': 'close',
                '最高': 'high',
                '最低': 'low',
                '成交量': 'volume',
                '成交额': 'amount'
            })
            
            return df
            
        except Exception as e:
            print(f"[Error] Failed to fetch minute data for {stock_code}: {e}")
            return pd.DataFrame()
    
    def get_stock_info(self, stock_code: str) -> Dict:
        """
        Get stock basic information
        
        Args:
            stock_code: Stock code
            
        Returns:
            Dictionary with stock basic info
        """
        try:
            df = ak.stock_individual_info_em(symbol=stock_code)
            info = {}
            for _, row in df.iterrows():
                info[row['item']] = row['value']
            return info
        except Exception as e:
            print(f"[Error] Failed to fetch stock info for {stock_code}: {e}")
            return {}
    
    def get_concept_list(self) -> pd.DataFrame:
        """Get concept sector list"""
        try:
            df = ak.stock_board_concept_name_em()
            return df
        except Exception as e:
            print(f"[Error] Failed to fetch concept list: {e}")
            return pd.DataFrame()
    
    def get_concept_stocks(self, concept_name: str) -> pd.DataFrame:
        """
        Get concept sector constituent stocks
        
        Args:
            concept_name: Concept sector name
            
        Returns:
            Constituent stocks list
        """
        try:
            df = ak.stock_board_concept_cons_em(symbol=concept_name)
            return df
        except Exception as e:
            print(f"[Error] Failed to fetch concept stocks for {concept_name}: {e}")
            return pd.DataFrame()
    
    def clear_cache(self):
        """Clear cache"""
        self.cache.clear()


# Test code
if __name__ == "__main__":
    fetcher = DataFetcher()
    
    # Test getting stock list
    print("Fetching stock list...")
    df_list = fetcher.get_stock_list()
    print(f"Got {len(df_list)} stocks")
    print(df_list.head())
    
    # Test getting daily data
    print("\nFetching daily data for 000001...")
    df_daily = fetcher.get_daily_data("000001")
    print(f"Got {len(df_daily)} records")
    print(df_daily.tail())
