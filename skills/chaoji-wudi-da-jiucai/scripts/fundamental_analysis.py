#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基本面分析脚本
分析：PE、PB、ROE、毛利率、成长能力、估值水平等
"""

import json
import sys
from datetime import datetime

def get_financial_metrics(code):
    """
    获取财务指标（模拟数据，实际应接入东方财富/同花顺 API）
    """
    # 这里应该调用真实的财务数据 API
    # 返回示例数据结构
    return {
        'code': code,
        'pe_ttm': None,  # 动态市盈率
        'pb': None,  # 市净率
        'roe': None,  # 净资产收益率
        'gross_margin': None,  # 毛利率
        'net_margin': None,  # 净利率
        'revenue_growth': None,  # 营收增长率
        'profit_growth': None,  # 净利润增长率
        'debt_ratio': None,  # 资产负债率
        'note': '财务数据需要接入付费 API，当前返回空值'
    }

def get_valuation_data(code):
    """
    获取估值数据
    """
    return {
        'code': code,
        'market_cap': None,  # 总市值
        'pe_percentile': None,  # PE 历史分位
        'pb_percentile': None,  # PB 历史分位
        'industry_pe': None,  # 行业平均 PE
        'industry_pb': None,  # 行业平均 PB
        'note': '估值数据需要接入付费 API'
    }

def get_shareholder_info(code):
    """
    获取股东信息
    """
    return {
        'code': code,
        'institution_holding': None,  # 机构持股比例
        'north_holding': None,  # 北向资金持股
        'major_shareholders': [],  # 前十大股东
        'note': '股东信息需要接入付费 API'
    }

def analyze_valuation(pe, pb, industry_pe, industry_pb, pe_percentile, pb_percentile):
    """
    分析估值水平
    """
    result = {
        'pe_status': '未知',
        'pb_status': '未知',
        'overall': '未知',
        'details': []
    }
    
    # PE 分析
    if pe and industry_pe:
        pe_ratio = pe / industry_pe
        if pe_ratio < 0.7:
            result['pe_status'] = '低估'
            result['details'].append(f'✅ PE 低于行业{round((1-pe_ratio)*100)}%')
        elif pe_ratio > 1.5:
            result['pe_status'] = '高估'
            result['details'].append(f'❌ PE 高于行业{round((pe_ratio-1)*100)}%')
        else:
            result['pe_status'] = '合理'
            result['details'].append(f'➖ PE 与行业持平')
    
    if pe_percentile:
        if pe_percentile < 30:
            result['details'].append(f'✅ PE 处于历史{pe_percentile}%分位（低估）')
        elif pe_percentile > 70:
            result['details'].append(f'❌ PE 处于历史{pe_percentile}%分位（高估）')
        else:
            result['details'].append(f'➖ PE 处于历史{pe_percentile}%分位（合理）')
    
    # PB 分析
    if pb and industry_pb:
        pb_ratio = pb / industry_pb
        if pb_ratio < 0.7:
            result['pb_status'] = '低估'
            result['details'].append(f'✅ PB 低于行业{round((1-pb_ratio)*100)}%')
        elif pb_ratio > 1.5:
            result['pb_status'] = '高估'
            result['details'].append(f'❌ PB 高于行业{round((pb_ratio-1)*100)}%')
        else:
            result['pb_status'] = '合理'
            result['details'].append(f'➖ PB 与行业持平')
    
    # 综合判断
    low_count = sum(1 for d in result['details'] if '✅' in d)
    high_count = sum(1 for d in result['details'] if '❌' in d)
    
    if low_count >= 2:
        result['overall'] = '低估'
    elif high_count >= 2:
        result['overall'] = '高估'
    else:
        result['overall'] = '合理'
    
    return result

def analyze_growth(revenue_growth, profit_growth):
    """
    分析成长能力
    """
    result = {
        'revenue_status': '未知',
        'profit_status': '未知',
        'overall': '未知',
        'details': []
    }
    
    if revenue_growth:
        if revenue_growth > 30:
            result['revenue_status'] = '高速增长'
            result['details'].append(f'✅ 营收增长{revenue_growth}%（高速）')
        elif revenue_growth > 10:
            result['revenue_status'] = '稳健增长'
            result['details'].append(f'✅ 营收增长{revenue_growth}%（稳健）')
        elif revenue_growth > 0:
            result['revenue_status'] = '低速增长'
            result['details'].append(f'➖ 营收增长{revenue_growth}%（低速）')
        else:
            result['revenue_status'] = '负增长'
            result['details'].append(f'❌ 营收下滑{abs(revenue_growth)}%')
    
    if profit_growth:
        if profit_growth > 30:
            result['profit_status'] = '高速增长'
            result['details'].append(f'✅ 利润增长{profit_growth}%（高速）')
        elif profit_growth > 10:
            result['profit_status'] = '稳健增长'
            result['details'].append(f'✅ 利润增长{profit_growth}%（稳健）')
        elif profit_growth > 0:
            result['profit_status'] = '低速增长'
            result['details'].append(f'➖ 利润增长{profit_growth}%（低速）')
        else:
            result['profit_status'] = '负增长'
            result['details'].append(f'❌ 利润下滑{abs(profit_growth)}%')
    
    # 综合判断
    if revenue_growth and profit_growth:
        if revenue_growth > 20 and profit_growth > 20:
            result['overall'] = '高成长'
        elif revenue_growth > 0 and profit_growth > 0:
            result['overall'] = '正成长'
        elif revenue_growth < 0 and profit_growth < 0:
            result['overall'] = '负成长'
        else:
            result['overall'] = '分化'
    
    return result

def analyze_profitability(roe, gross_margin, net_margin):
    """
    分析盈利能力
    """
    result = {
        'roe_status': '未知',
        'margin_status': '未知',
        'overall': '未知',
        'details': []
    }
    
    if roe:
        if roe > 20:
            result['roe_status'] = '优秀'
            result['details'].append(f'✅ ROE {roe}%（优秀）')
        elif roe > 10:
            result['roe_status'] = '良好'
            result['details'].append(f'✅ ROE {roe}%（良好）')
        elif roe > 5:
            result['roe_status'] = '一般'
            result['details'].append(f'➖ ROE {roe}%（一般）')
        else:
            result['roe_status'] = '较差'
            result['details'].append(f'❌ ROE {roe}%（较差）')
    
    if gross_margin:
        if gross_margin > 50:
            result['details'].append(f'✅ 毛利率{gross_margin}%（高）')
        elif gross_margin > 20:
            result['details'].append(f'➖ 毛利率{gross_margin}%（中）')
        else:
            result['details'].append(f'❌ 毛利率{gross_margin}%（低）')
    
    if net_margin:
        if net_margin > 20:
            result['details'].append(f'✅ 净利率{net_margin}%（高）')
        elif net_margin > 10:
            result['details'].append(f'➖ 净利率{net_margin}%（中）')
        else:
            result['details'].append(f'❌ 净利率{net_margin}%（低）')
    
    # 综合判断
    good_count = sum(1 for d in result['details'] if '✅' in d)
    bad_count = sum(1 for d in result['details'] if '❌' in d)
    
    if good_count >= 2:
        result['overall'] = '强'
    elif bad_count >= 2:
        result['overall'] = '弱'
    else:
        result['overall'] = '中等'
    
    return result

def fundamental_analysis(code, financial_data=None, valuation_data=None):
    """
    基本面综合分析
    """
    # 获取数据
    if not financial_data:
        financial_data = get_financial_metrics(code)
    if not valuation_data:
        valuation_data = get_valuation_data(code)
    
    # 估值分析
    valuation_result = analyze_valuation(
        financial_data.get('pe_ttm'),
        financial_data.get('pb'),
        valuation_data.get('industry_pe'),
        valuation_data.get('industry_pb'),
        valuation_data.get('pe_percentile'),
        valuation_data.get('pb_percentile')
    )
    
    # 成长分析
    growth_result = analyze_growth(
        financial_data.get('revenue_growth'),
        financial_data.get('profit_growth')
    )
    
    # 盈利能力分析
    profitability_result = analyze_profitability(
        financial_data.get('roe'),
        financial_data.get('gross_margin'),
        financial_data.get('net_margin')
    )
    
    # 综合评分
    score = 0
    max_score = 100
    
    # 估值分（30 分）
    if valuation_result['overall'] == '低估':
        score += 30
    elif valuation_result['overall'] == '合理':
        score += 20
    elif valuation_result['overall'] == '高估':
        score += 5
    
    # 成长分（40 分）
    if growth_result['overall'] == '高成长':
        score += 40
    elif growth_result['overall'] == '正成长':
        score += 25
    elif growth_result['overall'] == '分化':
        score += 15
    elif growth_result['overall'] == '负成长':
        score += 5
    
    # 盈利分（30 分）
    if profitability_result['overall'] == '强':
        score += 30
    elif profitability_result['overall'] == '中等':
        score += 20
    elif profitability_result['overall'] == '弱':
        score += 10
    
    # 评级
    if score >= 80:
        rating = '★★★★★'
        suggestion = '基本面优秀，值得关注'
    elif score >= 60:
        rating = '★★★★☆'
        suggestion = '基本面良好，可以考虑'
    elif score >= 40:
        rating = '★★★☆☆'
        suggestion = '基本面一般，谨慎观察'
    elif score >= 20:
        rating = '★★☆☆☆'
        suggestion = '基本面较差，注意风险'
    else:
        rating = '★☆☆☆☆'
        suggestion = '基本面弱，建议回避'
    
    return {
        'code': code,
        'score': score,
        'rating': rating,
        'suggestion': suggestion,
        'valuation': valuation_result,
        'growth': growth_result,
        'profitability': profitability_result,
        'financial_metrics': financial_data,
        'disclaimer': '基本面数据需要接入付费 API，当前分析基于有限数据'
    }

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法：python fundamental_analysis.py <股票代码>")
        sys.exit(1)
    
    code = sys.argv[1]
    result = fundamental_analysis(code)
    print(json.dumps(result, ensure_ascii=False, indent=2))
