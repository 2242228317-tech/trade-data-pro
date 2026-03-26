#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A 股行情数据获取脚本
数据源：新浪财经、腾讯财经、东方财富
"""

import requests
import json
import time
from datetime import datetime

# 股票代码转换（A 股需要添加前缀）
def format_stock_code(code):
    """格式化股票代码"""
    code = str(code).strip()
    if code.startswith('6'):
        return f'sh{code}'  # 上交所
    elif code.startswith('0') or code.startswith('3'):
        return f'sz{code}'  # 深交所
    return code

def get_realtime_quote(code):
    """
    获取实时行情数据（新浪财经）
    返回：开盘、收盘、最高、最低、成交量、成交额等
    """
    stock_code = format_stock_code(code)
    url = f'http://hq.sinajs.cn/sinajs.php?callback=callback&symbol={stock_code}'
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            # 解析返回数据
            data_str = response.text
            # 提取引号内的数据
            start = data_str.find('"') + 1
            end = data_str.rfind('"')
            if start > 0 and end > start:
                data = data_str[start:end].split(',')
                if len(data) >= 32:
                    return {
                        'code': code,
                        'name': data[0],
                        'open': float(data[1]) if data[1] else 0,
                        'close': float(data[2]) if data[2] else 0,  # 当前价
                        'high': float(data[33]) if len(data) > 33 and data[33] else float(data[3]) if data[3] else 0,
                        'low': float(data[34]) if len(data) > 34 and data[34] else float(data[4]) if data[4] else 0,
                        'volume': float(data[8]) if data[8] else 0,  # 成交量（手）
                        'amount': float(data[9]) if data[9] else 0,  # 成交额（元）
                        'bid': float(data[11]) if data[11] else 0,  # 买一价
                        'ask': float(data[21]) if data[21] else 0,  # 卖一价
                        'pre_close': float(data[2]) if data[2] else 0,  # 昨收
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
    except Exception as e:
        return {'error': str(e)}
    
    return {'error': '获取数据失败'}

def get_kline_history(code, period='day', count=100):
    """
    获取历史 K 线数据
    period: day(日 K), week(周 K), month(月 K)
    count: 获取条数
    """
    stock_code = format_stock_code(code)
    
    # 腾讯财经 API
    url = f'http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={stock_code},{period},,{count},qfq'
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'data' in data and stock_code in data['data']:
                kline_data = data['data'][stock_code]
                if period in kline_data:
                    klines = kline_data[period]
                    result = []
                    for k in klines:
                        result.append({
                            'date': k[0],
                            'open': float(k[1]),
                            'close': float(k[2]),
                            'high': float(k[3]),
                            'low': float(k[4]),
                            'volume': float(k[5]) if len(k) > 5 else 0
                        })
                    return {'code': code, 'klines': result}
    except Exception as e:
        return {'error': str(e)}
    
    return {'error': '获取 K 线失败'}

def get_stock_info(code):
    """
    获取股票基本信息
    """
    stock_code = format_stock_code(code)
    url = f'http://qt.gtimg.cn/q={stock_code}'
    
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data_str = response.text.decode('gbk') if isinstance(response.content, bytes) else response.text
            # 解析数据
            info = {}
            for line in data_str.split('\n'):
                if '~' in line:
                    parts = line.split('~')
                    if len(parts) >= 2:
                        key = parts[0].split('_')[-1] if '_' in parts[0] else parts[0]
                        info[key] = parts[1]
            return info
    except Exception as e:
        return {'error': str(e)}
    
    return {'error': '获取信息失败'}

def get_money_flow(code):
    """
    获取资金流向数据
    """
    # 这里可以接入同花顺或东方财富的资金流向 API
    # 简化版本，返回模拟数据
    return {
        'code': code,
        'main_force_in': 0,
        'main_force_out': 0,
        'net_inflow': 0,
        'note': '资金流向数据需要付费 API，当前为模拟数据'
    }

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python get_stock_data.py <股票代码> [数据类型]")
        print("数据类型：quote(行情), kline(K 线), info(信息), flow(资金)")
        sys.exit(1)
    
    code = sys.argv[1]
    data_type = sys.argv[2] if len(sys.argv) > 2 else 'quote'
    
    print(f"正在获取 {code} 的{data_type}数据...")
    
    if data_type == 'quote':
        result = get_realtime_quote(code)
    elif data_type == 'kline':
        result = get_kline_history(code)
    elif data_type == 'info':
        result = get_stock_info(code)
    elif data_type == 'flow':
        result = get_money_flow(code)
    else:
        print("未知数据类型")
        sys.exit(1)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
