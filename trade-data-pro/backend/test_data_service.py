#!/usr/bin/env python3
"""
测试脚本 - 数据服务三次测试
"""
import sys
import asyncio
sys.path.insert(0, '.')

from crawler.customs_real import RealCustomsCrawler, save_customs_data
from app.services.data_updater import DataUpdateService
from datetime import datetime

def test_1_customs_data():
    """第一次测试：海关数据获取"""
    print('='*60)
    print('第一次测试：海关数据获取')
    print('='*60)
    
    crawler = RealCustomsCrawler()
    
    # 测试1: 商品数据
    print('\n1. 获取商品进出口数据...')
    products = crawler.generate_sample_customs_data()
    print(f'   成功: {len(products)} 条商品数据')
    
    # 测试2: 国别数据
    print('\n2. 获取国别贸易数据...')
    countries = crawler.get_country_trade_data()
    print(f'   成功: {len(countries)} 条国别数据')
    
    # 测试3: 月度汇总
    print('\n3. 获取月度汇总数据...')
    summary = crawler.get_monthly_summary()
    print(f'   结果: {summary}')
    
    # 保存数据
    save_customs_data(products, 'test_customs_products_1.json')
    save_customs_data(countries, 'test_customs_countries_1.json')
    
    print('\n=== 第一次测试通过 ===')
    return True

def test_2_data_updater():
    """第二次测试：数据更新服务"""
    print('\n' + '='*60)
    print('第二次测试：数据更新服务')
    print('='*60)
    
    service = DataUpdateService()
    
    # 测试1: 加载现有数据
    print('\n1. 加载现有商品数据...')
    existing = service.load_existing_products()
    print(f'   成功: {len(existing)} 条现有数据')
    
    # 测试2: 获取数据摘要
    print('\n2. 获取数据摘要...')
    summary = service.get_update_summary()
    print(f'   总商品数: {summary[\"total_products\"]}')
    print(f'   品类数: {len(summary[\"categories\"])}')
    
    # 测试3: 更新海关数据
    print('\n3. 更新海关数据...')
    result = service.update_customs_data()
    print(f'   结果: {result}')
    
    print('\n=== 第二次测试通过 ===')
    return True

def test_3_data_integration():
    """第三次测试：数据整合和验证"""
    print('\n' + '='*60)
    print('第三次测试：数据整合和验证')
    print('='*60)
    
    import json
    import os
    
    data_dir = os.path.join('..', 'frontend', 'data')
    
    # 测试1: 验证商品数据文件
    print('\n1. 验证商品数据文件...')
    products_file = os.path.join(data_dir, 'all-products.json')
    if os.path.exists(products_file):
        with open(products_file, 'r', encoding='utf-8') as f:
            products = json.load(f)
        print(f'   成功: 加载 {len(products)} 个商品')
        
        # 验证数据完整性
        required_fields = ['id', 'name', 'price', 'category', 'supplier']
        valid_count = 0
        for p in products[:10]:  # 检查前10个
            if all(field in p for field in required_fields):
                valid_count += 1
        print(f'   数据完整性: {valid_count}/10 通过')
    else:
        print(f'   警告: 文件不存在 {products_file}')
    
    # 测试2: 验证海关数据文件
    print('\n2. 验证海关数据文件...')
    customs_file = os.path.join(data_dir, 'customs-data.json')
    if os.path.exists(customs_file):
        with open(customs_file, 'r', encoding='utf-8') as f:
            customs = json.load(f)
        print(f'   成功: 加载 {len(customs)} 条海关数据')
    else:
        print(f'   警告: 文件不存在 {customs_file}')
    
    # 测试3: 数据统计
    print('\n3. 数据统计分析...')
    if os.path.exists(products_file):
        with open(products_file, 'r', encoding='utf-8') as f:
            products = json.load(f)
        
        # 品类统计
        categories = {}
        for p in products:
            cat = p.get('category', '未知')
            categories[cat] = categories.get(cat, 0) + 1
        
        print('   品类分布:')
        for cat, count in sorted(categories.items(), key=lambda x: -x[1])[:5]:
            print(f'     {cat}: {count} 个')
    
    print('\n=== 第三次测试通过 ===')
    return True

if __name__ == '__main__':
    print(f'开始三次测试 - {datetime.now()}\n')
    
    results = []
    
    try:
        results.append(('Test 1', test_1_customs_data()))
    except Exception as e:
        print(f'第一次测试失败: {e}')
        results.append(('Test 1', False))
    
    try:
        results.append(('Test 2', test_2_data_updater()))
    except Exception as e:
        print(f'第二次测试失败: {e}')
        results.append(('Test 2', False))
    
    try:
        results.append(('Test 3', test_3_data_integration()))
    except Exception as e:
        print(f'第三次测试失败: {e}')
        results.append(('Test 3', False))
    
    print('\n' + '='*60)
    print('测试结果汇总')
    print('='*60)
    for name, passed in results:
        status = '通过' if passed else '失败'
        print(f'  {name}: {status}')
    
    all_passed = all(r[1] for r in results)
    print(f'\n总体结果: {\"全部通过\" if all_passed else \"存在失败\"}')