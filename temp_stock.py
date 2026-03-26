#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests

code = '002312'
url = f'http://qt.gtimg.cn/q=sz{code}'

response = requests.get(url, timeout=10)
response.encoding = 'gbk'
data = response.text

# 解析数据
if 'v_sz' in data:
    start = data.find('"') + 1
    end = data.rfind('"')
    fields = data[start:end].split('~')
    
    print(f"股票代码: {code}")
    print(f"股票名称: {fields[1]}")
    print(f"当前价格: {fields[3]} 元")
    print(f"昨收: {fields[4]} 元")
    print(f"今开: {fields[5]} 元")
    print(f"最高: {fields[33]} 元")
    print(f"最低: {fields[34]} 元")
    print(f"涨跌幅: {fields[32]}%")
    print(f"成交量: {int(fields[6])/10000:.2f} 万手")
    print(f"成交额: {round(float(fields[37])/10000, 2)} 万元")
    print(f"换手率: {fields[38]}%")
    print(f"市盈率: {fields[39]}")
    print(f"总市值: {round(float(fields[44])/100000000, 2)} 亿元")
    print(f"流通市值: {round(float(fields[45])/100000000, 2)} 亿元")

# 写入文件以便读取
with open('stock_result.txt', 'w', encoding='utf-8') as f:
    f.write(f"股票代码: {code}\n")
    f.write(f"股票名称: {fields[1]}\n")
    f.write(f"当前价格: {fields[3]} 元\n")
    f.write(f"昨收: {fields[4]} 元\n")
    f.write(f"今开: {fields[5]} 元\n")
    f.write(f"最高: {fields[33]} 元\n")
    f.write(f"最低: {fields[34]} 元\n")
    f.write(f"涨跌幅: {fields[32]}%\n")
    f.write(f"成交量: {int(fields[6])/10000:.2f} 万手\n")
    f.write(f"成交额: {round(float(fields[37])/10000, 2)} 万元\n")
    f.write(f"换手率: {fields[38]}%\n")
    f.write(f"市盈率: {fields[39]}\n")
    f.write(f"总市值: {round(float(fields[44])/100000000, 2)} 亿元\n")
    f.write(f"流通市值: {round(float(fields[45])/100000000, 2)} 亿元\n")
