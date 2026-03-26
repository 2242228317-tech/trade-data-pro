#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技术指标分析脚本
支持：均线、MACD、KDJ、RSI、BOLL 等常用指标
"""

import json
import sys
from datetime import datetime

def calculate_ma(prices, period):
    """计算移动平均线"""
    if len(prices) < period:
        return None
    return sum(prices[-period:]) / period

def calculate_ema(prices, period):
    """计算指数移动平均线"""
    if len(prices) < period:
        return None
    
    multiplier = 2 / (period + 1)
    ema = sum(prices[:period]) / period
    
    for price in prices[period:]:
        ema = (price - ema) * multiplier + ema
    
    return ema

def calculate_macd(prices, short=12, long=26, signal=9):
    """
    计算 MACD 指标
    返回：DIF, DEA, MACD 柱
    """
    if len(prices) < long + signal:
        return None
    
    # 计算 EMA
    ema_short = calculate_ema(prices[-short:], short)
    ema_long = calculate_ema(prices[-long:], long)
    
    if ema_short is None or ema_long is None:
        return None
    
    dif = ema_short - ema_long
    
    # 计算 DEA（DIF 的 EMA）
    dif_values = []
    for i in range(signal):
        idx = len(prices) - signal + i
        if idx >= long:
            es = calculate_ema(prices[:idx+1], short)
            el = calculate_ema(prices[:idx+1], long)
            if es and el:
                dif_values.append(es - el)
    
    if len(dif_values) < signal:
        dea = dif
    else:
        dea = calculate_ema(dif_values, signal)
    
    macd_bar = 2 * (dif - dea)
    
    return {
        'dif': round(dif, 4),
        'dea': round(dea, 4),
        'macd': round(macd_bar, 4)
    }

def calculate_kdj(highs, lows, closes, n=9, m1=3, m2=3):
    """
    计算 KDJ 指标
    返回：K, D, J
    """
    if len(closes) < n:
        return None
    
    # 计算 RSV
    lowest = min(lows[-n:])
    highest = max(highs[-n:])
    
    if highest == lowest:
        rsv = 50
    else:
        rsv = (closes[-1] - lowest) / (highest - lowest) * 100
    
    # 简化计算，实际应该用 EMA
    k = rsv
    d = k
    j = 3 * k - 2 * d
    
    return {
        'k': round(k, 2),
        'd': round(d, 2),
        'j': round(j, 2)
    }

def calculate_rsi(prices, period=14):
    """
    计算 RSI 指标
    返回：RSI 值 (0-100)
    """
    if len(prices) < period + 1:
        return None
    
    gains = []
    losses = []
    
    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        if change > 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))
    
    if len(gains) < period:
        return None
    
    avg_gain = sum(gains[-period:]) / period
    avg_loss = sum(losses[-period:]) / period
    
    if avg_loss == 0:
        return 100
    
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return round(rsi, 2)

def calculate_boll(prices, period=20, std_dev=2):
    """
    计算布林带
    返回：上轨、中轨、下轨
    """
    if len(prices) < period:
        return None
    
    # 中轨 = MA
    middle = calculate_ma(prices, period)
    
    # 计算标准差
    mean = middle
    variance = sum((p - mean) ** 2 for p in prices[-period:]) / period
    std = variance ** 0.5
    
    upper = middle + std_dev * std
    lower = middle - std_dev * std
    
    return {
        'upper': round(upper, 2),
        'middle': round(middle, 2),
        'lower': round(lower, 2)
    }

def analyze_signals(macd, kdj, rsi, boll, current_price):
    """
    分析技术指标信号
    返回：买入/卖出信号、超买超卖状态
    """
    signals = []
    status = {
        'trend': '未知',
        'strength': '中性',
        'suggestions': []
    }
    
    # MACD 信号
    if macd:
        if macd['macd'] > 0 and macd['dif'] > macd['dea']:
            signals.append('MACD 金叉，多头信号')
            status['suggestions'].append('✅ MACD 多头')
        elif macd['macd'] < 0 and macd['dif'] < macd['dea']:
            signals.append('MACD 死叉，空头信号')
            status['suggestions'].append('❌ MACD 空头')
    
    # KDJ 信号
    if kdj:
        if kdj['j'] < 0:
            signals.append('KDJ 超卖，可能反弹')
            status['suggestions'].append('⚠️ KDJ 超卖')
        elif kdj['j'] > 100:
            signals.append('KDJ 超买，可能回调')
            status['suggestions'].append('⚠️ KDJ 超买')
        elif kdj['k'] > kdj['d']:
            status['suggestions'].append('✅ KDJ 金叉')
        else:
            status['suggestions'].append('❌ KDJ 死叉')
    
    # RSI 信号
    if rsi:
        if rsi < 20:
            signals.append('RSI 严重超卖')
            status['suggestions'].append('⚠️ RSI 超卖区')
        elif rsi > 80:
            signals.append('RSI 严重超买')
            status['suggestions'].append('⚠️ RSI 超买区')
        elif 40 <= rsi <= 60:
            status['suggestions'].append('➖ RSI 中性')
    
    # 布林带信号
    if boll:
        if current_price < boll['lower']:
            signals.append('股价跌破下轨，可能反弹')
            status['suggestions'].append('✅ 布林带下轨支撑')
        elif current_price > boll['upper']:
            signals.append('股价突破上轨，可能回调')
            status['suggestions'].append('❌ 布林带上轨压力')
        else:
            status['suggestions'].append('➖ 布林带内震荡')
    
    # 综合判断
    buy_count = sum(1 for s in status['suggestions'] if '✅' in s)
    sell_count = sum(1 for s in status['suggestions'] if '❌' in s)
    
    if buy_count > sell_count + 1:
        status['trend'] = '偏多'
        status['strength'] = '较强'
    elif sell_count > buy_count + 1:
        status['trend'] = '偏空'
        status['strength'] = '较强'
    else:
        status['trend'] = '震荡'
        status['strength'] = '中性'
    
    return {
        'signals': signals,
        'status': status
    }

def technical_analysis(klines):
    """
    对 K 线数据进行技术分析
    """
    if not klines or len(klines) < 30:
        return {'error': 'K 线数据不足'}
    
    # 提取价格序列
    closes = [k['close'] for k in klines]
    highs = [k['high'] for k in klines]
    lows = [k['low'] for k in klines]
    opens = [k['open'] for k in klines]
    
    current_price = closes[-1]
    
    # 计算各指标
    ma5 = calculate_ma(closes, 5)
    ma10 = calculate_ma(closes, 10)
    ma20 = calculate_ma(closes, 20)
    ma60 = calculate_ma(closes, 60) if len(closes) >= 60 else None
    
    macd = calculate_macd(closes)
    kdj = calculate_kdj(highs, lows, closes)
    rsi = calculate_rsi(closes)
    boll = calculate_boll(closes)
    
    # 分析信号
    signals = analyze_signals(macd, kdj, rsi, boll, current_price)
    
    # 均线分析
    ma_analysis = []
    if ma5 and ma10:
        if ma5 > ma10:
            ma_analysis.append('短期均线多头排列')
        else:
            ma_analysis.append('短期均线空头排列')
    
    if ma20:
        if current_price > ma20:
            ma_analysis.append('股价在 20 日均线上方')
        else:
            ma_analysis.append('股价在 20 日均线下方')
    
    return {
        'current_price': current_price,
        'moving_averages': {
            'ma5': round(ma5, 2) if ma5 else None,
            'ma10': round(ma10, 2) if ma10 else None,
            'ma20': round(ma20, 2) if ma20 else None,
            'ma60': round(ma60, 2) if ma60 else None
        },
        'macd': macd,
        'kdj': kdj,
        'rsi': rsi,
        'boll': boll,
        'ma_analysis': ma_analysis,
        'signals': signals['signals'],
        'status': signals['status']
    }

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法：python technical_analysis.py <K 线数据 JSON 文件>")
        print("或：python technical_analysis.py --demo")
        sys.exit(1)
    
    if sys.argv[1] == '--demo':
        # 演示数据
        import random
        base_price = 100
        klines = []
        for i in range(100):
            change = random.uniform(-0.05, 0.05)
            close = base_price * (1 + change)
            high = close * random.uniform(1, 1.03)
            low = close * random.uniform(0.97, 1)
            klines.append({
                'date': f'2024-{(i//30)%12+1:02d}-{i%30+1:02d}',
                'open': round(base_price, 2),
                'close': round(close, 2),
                'high': round(high, 2),
                'low': round(low, 2),
                'volume': random.randint(10000, 100000)
            })
            base_price = close
        
        result = technical_analysis(klines)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 从文件读取 K 线数据
        with open(sys.argv[1], 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        klines = data.get('klines', [])
        result = technical_analysis(klines)
        print(json.dumps(result, ensure_ascii=False, indent=2))
