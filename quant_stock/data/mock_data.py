"""
Mock data provider for demo/testing purposes
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def generate_mock_daily_data(stock_code: str, days: int = 100) -> pd.DataFrame:
    """
    Generate mock daily stock data for demonstration
    
    Args:
        stock_code: Stock code
        days: Number of days to generate
        
    Returns:
        DataFrame with OHLCV data
    """
    np.random.seed(hash(stock_code) % 2**32)
    
    # Generate consecutive dates
    end_date = datetime.now()
    dates = []
    current = end_date - timedelta(days=days*2)  # Start earlier to get enough business days
    while len(dates) < days and current <= end_date:
        if current.weekday() < 5:  # Monday = 0, Friday = 4
            dates.append(current)
        current += timedelta(days=1)
    
    dates = dates[-days:]  # Take the last 'days' dates
    
    # Generate realistic price movement
    base_price = np.random.uniform(10, 100)
    returns = np.random.normal(0.001, 0.02, days)
    prices = base_price * np.exp(np.cumsum(returns))
    
    # Generate OHLC from close prices
    df = pd.DataFrame({
        'date': dates,
        'close': prices
    })
    
    df['high'] = df['close'] * (1 + np.abs(np.random.normal(0, 0.01, days)))
    df['low'] = df['close'] * (1 - np.abs(np.random.normal(0, 0.01, days)))
    df['open'] = df['close'].shift(1) * (1 + np.random.normal(0, 0.005, days))
    df['open'] = df['open'].fillna(df['close'] * 0.99)
    
    # Volume
    df['volume'] = np.random.randint(1000000, 10000000, days)
    df['amount'] = df['volume'] * df['close']
    
    # Price change
    df['pct_change'] = df['close'].pct_change() * 100
    df['change'] = df['close'].diff()
    
    # Ensure OHLC consistency
    df['high'] = df[['open', 'close', 'high']].max(axis=1)
    df['low'] = df[['open', 'close', 'low']].min(axis=1)
    
    return df.sort_values('date').reset_index(drop=True)


def get_mock_stock_list(n: int = 100) -> pd.DataFrame:
    """Generate mock stock list"""
    codes = [f"{i:06d}" for i in range(1, n+1)]
    names = [f"Stock_{i}" for i in range(1, n+1)]
    
    df = pd.DataFrame({
        'code': codes,
        'name': names,
        'price': np.random.uniform(10, 100, n),
        'change_pct': np.random.uniform(-10, 10, n),
        'volume': np.random.randint(1000000, 10000000, n),
        'amount': np.random.randint(10000000, 100000000, n)
    })
    
    return df
