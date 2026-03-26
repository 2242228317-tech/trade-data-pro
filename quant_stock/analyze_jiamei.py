"""
嘉美包装 (002969) 真实数据分析
使用 baostock 数据源
"""

import baostock as bs
import pandas as pd
import numpy as np
from datetime import datetime


def calculate_ma(df, periods=[5, 10, 20, 60]):
    """Calculate moving averages"""
    for period in periods:
        df[f'MA{period}'] = df['close'].rolling(window=period).mean()
    return df


def calculate_macd(df, fast=12, slow=26, signal=9):
    """Calculate MACD"""
    ema_fast = df['close'].ewm(span=fast, adjust=False).mean()
    ema_slow = df['close'].ewm(span=slow, adjust=False).mean()
    df['DIF'] = ema_fast - ema_slow
    df['DEA'] = df['DIF'].ewm(span=signal, adjust=False).mean()
    df['MACD'] = (df['DIF'] - df['DEA']) * 2
    return df


def calculate_kdj(df, n=9, m1=3, m2=3):
    """Calculate KDJ"""
    lowest_low = df['low'].rolling(window=n).min()
    highest_high = df['high'].rolling(window=n).max()
    df['RSV'] = (df['close'] - lowest_low) / (highest_high - lowest_low) * 100
    df['K'] = df['RSV'].ewm(com=m1-1, adjust=False).mean()
    df['D'] = df['K'].ewm(com=m2-1, adjust=False).mean()
    df['J'] = 3 * df['K'] - 2 * df['D']
    return df


def calculate_rsi(df, periods=[6, 12, 24]):
    """Calculate RSI"""
    for period in periods:
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()
        rs = avg_gain / avg_loss
        df[f'RSI{period}'] = 100 - (100 / (1 + rs))
    return df


def calculate_boll(df, period=20, width=2.0):
    """Calculate Bollinger Bands"""
    df['BOLL_MID'] = df['close'].rolling(window=period).mean()
    std = df['close'].rolling(window=period).std()
    df['BOLL_UPPER'] = df['BOLL_MID'] + width * std
    df['BOLL_LOWER'] = df['BOLL_MID'] - width * std
    return df


def analyze_stock(stock_code='002969', stock_name='嘉美包装'):
    """Analyze stock with real data from baostock"""
    
    print("=" * 60)
    print(f"Stock Analysis: {stock_name} ({stock_code})")
    print("Data Source: Baostock (Real Data)")
    print("=" * 60)
    
    # Login to baostock
    lg = bs.login()
    if lg.error_code != '0':
        print(f"Login failed: {lg.error_msg}")
        return
    
    # Format code
    if stock_code.startswith('6'):
        bs_code = f"{stock_code}.sh"
    else:
        bs_code = f"{stock_code}.sz"
    
    # Query data (last 100 days)
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - pd.Timedelta(days=120)).strftime('%Y-%m-%d')
    
    rs = bs.query_history_k_data_plus(
        bs_code,
        "date,open,high,low,close,volume",
        start_date=start_date,
        end_date=end_date,
        frequency="d",
        adjustflag="3"
    )
    
    # Get data
    data_list = []
    while (rs.error_code == '0') and rs.next():
        data_list.append(rs.get_row_data())
    
    bs.logout()
    
    if len(data_list) == 0:
        print("No data retrieved")
        return
    
    # Create DataFrame
    df = pd.DataFrame(data_list, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    df['date'] = pd.to_datetime(df['date'])
    
    # Replace empty strings with NaN and convert to float
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Drop rows with NaN values
    df = df.dropna()
    
    if len(df) == 0:
        print("No valid data retrieved")
        return
    
    # Calculate indicators
    df = calculate_ma(df)
    df = calculate_macd(df)
    df = calculate_kdj(df)
    df = calculate_rsi(df)
    df = calculate_boll(df)
    
    # Get latest data
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else latest
    
    # Calculate price change
    pct_change = (latest['close'] - prev['close']) / prev['close'] * 100
    
    # Display results
    print(f"\n[Basic Data] (As of {latest['date'].strftime('%Y-%m-%d')})")
    print(f"   Open:     {latest['open']:.2f}")
    print(f"   High:     {latest['high']:.2f}")
    print(f"   Low:      {latest['low']:.2f}")
    print(f"   Close:    {latest['close']:.2f}")
    print(f"   Change:   {pct_change:+.2f}%")
    print(f"   Volume:   {latest['volume']:,.0f}")
    
    # Moving averages
    print(f"\n[Moving Averages]")
    print(f"   MA5:  {latest['MA5']:.2f}")
    print(f"   MA10: {latest['MA10']:.2f}")
    print(f"   MA20: {latest['MA20']:.2f}")
    print(f"   MA60: {latest['MA60']:.2f}")
    
    # Trend judgment
    if (latest['MA5'] > latest['MA10'] > latest['MA20'] > latest['MA60']):
        print("   [OK] Bullish Alignment")
    elif (latest['MA5'] < latest['MA10'] < latest['MA20'] < latest['MA60']):
        print("   [X] Bearish Alignment")
    else:
        print("   [!] Mixed Alignment")
    
    # MACD
    print(f"\n[MACD Indicator]")
    print(f"   DIF:   {latest['DIF']:.4f}")
    print(f"   DEA:   {latest['DEA']:.4f}")
    print(f"   MACD:  {latest['MACD']:.4f}")
    
    if latest['DIF'] > latest['DEA']:
        if prev['DIF'] <= prev['DEA']:
            print("   [OK] Golden Cross (New)")
        else:
            print("   [OK] Golden Cross State")
    else:
        if prev['DIF'] >= prev['DEA']:
            print("   [X] Dead Cross (New)")
        else:
            print("   [X] Dead Cross State")
    
    # KDJ
    print(f"\n[KDJ Indicator]")
    print(f"   K: {latest['K']:.2f}")
    print(f"   D: {latest['D']:.2f}")
    print(f"   J: {latest['J']:.2f}")
    
    if latest['K'] > 80:
        print("   [!] Overbought Zone")
    elif latest['K'] < 20:
        print("   [OK] Oversold Zone")
    
    # RSI
    print(f"\n[RSI Indicator]")
    print(f"   RSI6:  {latest['RSI6']:.2f}")
    print(f"   RSI12: {latest['RSI12']:.2f}")
    print(f"   RSI24: {latest['RSI24']:.2f}")
    
    # Bollinger Bands
    print(f"\n[Bollinger Bands]")
    print(f"   Upper: {latest['BOLL_UPPER']:.2f}")
    print(f"   Mid:   {latest['BOLL_MID']:.2f}")
    print(f"   Lower: {latest['BOLL_LOWER']:.2f}")
    
    if latest['close'] > latest['BOLL_UPPER']:
        print("   [!] Above Upper Band")
    elif latest['close'] < latest['BOLL_LOWER']:
        print("   [OK] Below Lower Band (Possible Oversold)")
    
    # Trading suggestions
    print(f"\n[Trading Suggestions]")
    support_short = df['low'].iloc[-5:].min()
    support_mid = df['low'].iloc[-20:].min()
    print(f"   Support:  {support_short:.2f} (Short), {support_mid:.2f} (Mid)")
    
    resistance_short = df['high'].iloc[-5:].max()
    resistance_mid = df['high'].iloc[-20:].max()
    print(f"   Resist:   {resistance_short:.2f} (Short), {resistance_mid:.2f} (Mid)")
    
    stop_loss = latest['close'] * 0.95
    print(f"   StopLoss: {stop_loss:.2f} (-5%)")
    
    # Overall score
    score = 0
    reasons = []
    
    if latest['MA5'] > latest['MA10']:
        score += 1
        reasons.append("MA5>MA10")
    if latest['DIF'] > latest['DEA']:
        score += 1
        reasons.append("MACD Golden")
    if latest['K'] > latest['D']:
        score += 1
        reasons.append("KDJ Golden")
    if latest['close'] > latest['MA20']:
        score += 1
        reasons.append("Above MA20")
    if latest['volume'] > df['volume'].iloc[-10:].mean():
        score += 1
        reasons.append("Volume Up")
    
    print(f"\n[Overall Score]: {score}/5")
    if reasons:
        print(f"   Reasons: {', '.join(reasons)}")
    
    if score >= 4:
        print(f"   [OK] Suggestion: Consider Entry")
    elif score >= 2:
        print(f"   [-] Suggestion: Wait & See")
    else:
        print(f"   [X] Suggestion: Avoid")
    
    print("\n" + "=" * 60)
    print("Disclaimer: For reference only, not investment advice!")
    print("=" * 60)


if __name__ == "__main__":
    analyze_stock('002969', '嘉美包装')
