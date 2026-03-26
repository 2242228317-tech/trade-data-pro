#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import akshare as ak

print("="*50)
print("002312 川发龙蟒 股票分析")
print("="*50)

# 腾讯财经获取实时数据
code = '002312'
url = f'http://qt.gtimg.cn/q=sz{code}'

try:
    response = requests.get(url, timeout=10)
    response.encoding = 'gbk'
    data = response.text
    
    start = data.find('"') + 1
    end = data.rfind('"')
    fields = data[start:end].split('~')
    
    print("\n【实时行情】")
    print(f"  股票名称: {fields[1]}")
    print(f"  当前价格: {fields[3]} 元")
    print(f"  昨收: {fields[4]} 元")
    print(f"  今开: {fields[5]} 元")
    print(f"  最高: {fields[33]} 元")
    print(f"  最低: {fields[34]} 元")
    print(f"  涨跌幅: {fields[32]}%")
    print(f"  涨跌额: {fields[31]} 元")
    print(f"  成交量: {int(int(fields[6])/10000)} 万手")
    print(f"  成交额: {round(float(fields[37])/10000, 2)} 万元")
    print(f"  换手率: {fields[38]}%")
    print(f"  振幅: {fields[43]}%")
    print(f"  市盈率: {fields[39]}")
    
except Exception as e:
    print(f"实时行情获取失败: {e}")

# 近5日K线
print("\n" + "="*50)
print("【近5日走势】")
try:
    df_kline = ak.stock_zh_a_hist(symbol=code, period="daily", start_date="20250301", adjust="qfq")
    recent = df_kline.tail(5)
    for idx, row in recent.iterrows():
        change_pct = (row['收盘'] - row['开盘']) / row['开盘'] * 100
        print(f"  {row['日期']}: 开{row['开盘']:.2f} 收{row['收盘']:.2f} ({change_pct:+.2f}%) 高{row['最高']:.2f} 低{row['最低']:.2f}")
except Exception as e:
    print(f"K线数据获取失败: {e}")

# 资金流向
print("\n" + "="*50)
print("【资金流向】(今日)")
try:
    df_flow = ak.stock_individual_fund_flow(stock=code, market="sz")
    latest = df_flow.iloc[0]
    print(f"  主力净流入: {latest['主力净流入-净额']/10000:.2f}万元 ({latest['主力净流入-净占比']:+.2f}%)")
    print(f"  超大单净流入: {latest['超大单净流入-净额']/10000:.2f}万元 ({latest['超大单净流入-净占比']:+.2f}%)")
    print(f"  大单净流入: {latest['大单净流入-净额']/10000:.2f}万元 ({latest['大单净流入-净占比']:+.2f}%)")
    print(f"  中单净流入: {latest['中单净流入-净额']/10000:.2f}万元 ({latest['中单净流入-净占比']:+.2f}%)")
    print(f"  小单净流入: {latest['小单净流入-净额']/10000:.2f}万元 ({latest['小单净流入-净占比']:+.2f}%)")
except Exception as e:
    print(f"资金流向获取失败: {e}")

print("\n" + "="*50)
