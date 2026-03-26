#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import akshare as ak
import json

# 获取实时行情
code = "002312"
name = "川发龙蟒"

print(f"股票代码: {code}")
print(f"股票名称: {name}")
print("="*50)

# 获取最新行情
try:
    df_spot = ak.stock_zh_a_spot_em()
    stock_info = df_spot[df_spot['代码'] == code]
    if not stock_info.empty:
        print("\n【实时行情】")
        info_cols = ['最新价', '涨跌幅', '涨跌额', '成交量', '成交额', '振幅', '最高', '最低', '今开', '昨收', '换手率', '市盈率-动态', '总市值', '流通市值']
        for col in info_cols:
            if col in stock_info.columns:
                val = stock_info[col].values[0]
                print(f"  {col}: {val}")
except Exception as e:
    print(f"行情数据获取失败: {e}")

# 获取历史K线数据
try:
    print("\n" + "="*50)
    print("\n【近5日K线数据】")
    df_kline = ak.stock_zh_a_hist(symbol=code, period="daily", start_date="20250301", adjust="qfq")
    recent = df_kline.tail(5)
    for idx, row in recent.iterrows():
        print(f"  {row['日期']}: 开{row['开盘']:.2f} 收{row['收盘']:.2f} 高{row['最高']:.2f} 低{row['最低']:.2f} 量{row['成交量']/10000:.0f}万")
except Exception as e:
    print(f"K线数据获取失败: {e}")

# 获取资金流向
try:
    print("\n" + "="*50)
    print("\n【今日资金流向】")
    df_flow = ak.stock_individual_fund_flow(stock=code, market="sz")
    latest = df_flow.iloc[0]
    print(f"  日期: {latest['日期']}")
    print(f"  主力净流入: {latest['主力净流入-净额']/10000:.2f}万")
    print(f"  超大单净流入: {latest['超大单净流入-净额']/10000:.2f}万")
    print(f"  大单净流入: {latest['大单净流入-净额']/10000:.2f}万")
    print(f"  中单净流入: {latest['中单净流入-净额']/10000:.2f}万")
    print(f"  小单净流入: {latest['小单净流入-净额']/10000:.2f}万")
    print(f"  主力净流入占比: {latest['主力净流入-净占比']:.2f}%")
except Exception as e:
    print(f"资金流向获取失败: {e}")
