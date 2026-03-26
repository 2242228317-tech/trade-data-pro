#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
风险评估脚本
分析：波动率、最大回撤、估值风险、行业风险等
"""

import json
import sys
from datetime import datetime
import math

def calculate_volatility(prices, period=20):
    """
    计算波动率（年化）
    """
    if len(prices) < period + 1:
        return None
    
    # 计算日收益率
    returns = []
    for i in range(1, len(prices)):
        ret = (prices[i] - prices[i-1]) / prices[i-1]
        returns.append(ret)
    
    # 计算标准差
    mean_ret = sum(returns[-period:]) / period
    variance = sum((r - mean_ret) ** 2 for r in returns[-period:]) / period
    daily_std = math.sqrt(variance)
    
    # 年化波动率
    annual_vol = daily_std * math.sqrt(252) * 100
    
    return round(annual_vol, 2)

def calculate_max_drawdown(prices):
    """
    计算最大回撤
    """
    if len(prices) < 2:
        return None
    
    peak = prices[0]
    max_dd = 0
    
    for price in prices:
        if price > peak:
            peak = price
        drawdown = (peak - price) / peak * 100
        if drawdown > max_dd:
            max_dd = drawdown
    
    return round(max_dd, 2)

def analyze_price_position(current_price, klines):
    """
    分析股价位置（历史分位）
    """
    if not klines or len(klines) < 60:
        return None
    
    closes = [k['close'] for k in klines]
    high_52w = max(closes[-252:]) if len(closes) >= 252 else max(closes)
    low_52w = min(closes[-252:]) if len(closes) >= 252 else min(closes)
    
    if high_52w == low_52w:
        return 50
    
    position = (current_price - low_52w) / (high_52w - low_52w) * 100
    
    return round(position, 2)

def check_risk_signals(klines, current_price, pe=None, industry_pe=None):
    """
    检查风险信号
    """
    risks = []
    risk_level = '低'
    risk_score = 0
    
    if not klines or len(klines) < 30:
        return {'risks': ['数据不足'], 'level': '未知', 'score': 0}
    
    closes = [k['close'] for k in klines]
    
    # 1. 高位风险
    position = analyze_price_position(current_price, klines)
    if position and position > 80:
        risks.append({
            'type': '高位风险',
            'level': '高',
            'desc': f'股价处于 52 周{position}%分位（高位）',
            'score': 25
        })
        risk_score += 25
    elif position and position > 60:
        risks.append({
            'type': '中高位',
            'level': '中',
            'desc': f'股价处于 52 周{position}%分位（中高位）',
            'score': 10
        })
        risk_score += 10
    
    # 2. 波动率风险
    volatility = calculate_volatility(closes)
    if volatility:
        if volatility > 60:
            risks.append({
                'type': '高波动',
                'level': '高',
                'desc': f'年化波动率{volatility}%（很高）',
                'score': 20
            })
            risk_score += 20
        elif volatility > 40:
            risks.append({
                'type': '中高波动',
                'level': '中',
                'desc': f'年化波动率{volatility}%（较高）',
                'score': 10
            })
            risk_score += 10
    
    # 3. 回撤风险
    max_dd = calculate_max_drawdown(closes)
    if max_dd:
        if max_dd > 40:
            risks.append({
                'type': '大回撤',
                'level': '高',
                'desc': f'历史最大回撤{max_dd}%（很大）',
                'score': 20
            })
            risk_score += 20
        elif max_dd > 25:
            risks.append({
                'type': '中回撤',
                'level': '中',
                'desc': f'历史最大回撤{max_dd}%（较大）',
                'score': 10
            })
            risk_score += 10
    
    # 4. 估值风险
    if pe and industry_pe:
        pe_ratio = pe / industry_pe
        if pe_ratio > 2:
            risks.append({
                'type': '高估值',
                'level': '高',
                'desc': f'PE 是行业{round(pe_ratio, 1)}倍（显著高估）',
                'score': 25
            })
            risk_score += 25
        elif pe_ratio > 1.5:
            risks.append({
                'type': '中高估值',
                'level': '中',
                'desc': f'PE 是行业{round(pe_ratio, 1)}倍（偏高）',
                'score': 10
            })
            risk_score += 10
    
    # 5. 技术破位风险
    if len(closes) >= 20:
        ma20 = sum(closes[-20:]) / 20
        if current_price < ma20 * 0.9:
            risks.append({
                'type': '技术破位',
                'level': '高',
                'desc': '股价跌破 20 日均线 10% 以上',
                'score': 20
            })
            risk_score += 20
        elif current_price < ma20:
            risks.append({
                'type': '均线压制',
                'level': '中',
                'desc': '股价在 20 日均线下方',
                'score': 10
            })
            risk_score += 10
    
    # 综合风险等级
    if risk_score >= 60:
        risk_level = '高'
    elif risk_score >= 30:
        risk_level = '中'
    else:
        risk_level = '低'
    
    return {
        'risks': risks,
        'level': risk_level,
        'score': risk_score,
        'volatility': volatility,
        'max_drawdown': max_dd,
        'position': position
    }

def generate_stop_loss_suggestions(current_price, klines, risk_level):
    """
    生成止盈止损建议
    """
    if not klines or len(klines) < 20:
        return {}
    
    closes = [k['close'] for k in klines]
    
    # 支撑位（近期低点）
    support = min(closes[-20:])
    # 压力位（近期高点）
    resistance = max(closes[-20:])
    # 均线
    ma20 = sum(closes[-20:]) / 20
    
    suggestions = {
        'support': round(support, 2),
        'resistance': round(resistance, 2),
        'ma20': round(ma20, 2)
    }
    
    # 止损建议
    if risk_level == '高':
        stop_loss = current_price * 0.92  # 8% 止损
        suggestions['stop_loss'] = round(stop_loss, 2)
        suggestions['stop_loss_pct'] = '8%'
    elif risk_level == '中':
        stop_loss = current_price * 0.95  # 5% 止损
        suggestions['stop_loss'] = round(stop_loss, 2)
        suggestions['stop_loss_pct'] = '5%'
    else:
        stop_loss = current_price * 0.90  # 10% 止损
        suggestions['stop_loss'] = round(stop_loss, 2)
        suggestions['stop_loss_pct'] = '10%'
    
    # 止盈建议
    take_profit = current_price * 1.15  # 15% 止盈
    suggestions['take_profit'] = round(take_profit, 2)
    suggestions['take_profit_pct'] = '15%'
    
    return suggestions

def risk_assessment(code, klines, current_price, pe=None, industry_pe=None):
    """
    综合风险评估
    """
    # 风险信号分析
    risk_result = check_risk_signals(klines, current_price, pe, industry_pe)
    
    # 止盈止损建议
    stop_suggestions = generate_stop_loss_suggestions(
        current_price, klines, risk_result['level']
    )
    
    # 仓位建议
    if risk_result['level'] == '高':
        position_suggestion = '建议轻仓（<30%）或观望'
        max_position = 30
    elif risk_result['level'] == '中':
        position_suggestion = '建议中等仓位（30-50%）'
        max_position = 50
    else:
        position_suggestion = '可适当重仓（50-70%）'
        max_position = 70
    
    # 操作建议
    if risk_result['level'] == '高' and len(risk_result['risks']) >= 3:
        action = '⚠️ 风险较高，建议谨慎或回避'
    elif risk_result['level'] == '高':
        action = '⚠️ 注意风险，严格止损'
    elif risk_result['level'] == '中':
        action = '➖ 风险可控，可逢低布局'
    else:
        action = '✅ 风险较低，可积极关注'
    
    return {
        'code': code,
        'current_price': current_price,
        'risk_level': risk_result['level'],
        'risk_score': risk_result['score'],
        'risk_factors': risk_result['risks'],
        'volatility': risk_result.get('volatility'),
        'max_drawdown': risk_result.get('max_drawdown'),
        'price_position': risk_result.get('position'),
        'stop_suggestions': stop_suggestions,
        'position_suggestion': position_suggestion,
        'max_position': max_position,
        'action': action,
        'disclaimer': '风险评估仅供参考，不构成投资建议'
    }

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法：python risk_checker.py <股票代码>")
        print("或：python risk_checker.py --demo")
        sys.exit(1)
    
    if sys.argv[1] == '--demo':
        # 演示数据
        import random
        base_price = 50
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
        
        current_price = klines[-1]['close']
        result = risk_assessment('demo', klines, current_price)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        code = sys.argv[1]
        # 实际使用需要传入 K 线数据
        print(f"请提供 {code} 的 K 线数据")
