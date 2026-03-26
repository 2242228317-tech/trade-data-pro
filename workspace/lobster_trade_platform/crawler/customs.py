"""
海关数据爬虫
爬取中国海关出口数据
"""

import requests
import time
import sqlite3
from datetime import datetime

DATABASE = 'database/trade_data.db'

class CustomsCrawler:
    """海关数据爬虫"""
    
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        }
    
    def crawl(self):
        """
        爬取海关出口数据
        使用模拟数据演示
        """
        print("[CustomsCrawler] Starting crawl")
        
        # 模拟海关数据（龙虾相关产品）
        mock_data = [
            {
                'product_name': '活、鲜或冷的龙虾',
                'category': '甲壳类',
                'hs_code': '03063100',
                'export_value': 156800000,
                'export_weight': 5200,
                'unit': '吨',
                'destination_country': '美国',
                'trade_month': '2025-02'
            },
            {
                'product_name': '冻龙虾',
                'category': '甲壳类',
                'hs_code': '03061100',
                'export_value': 128500000,
                'export_weight': 6800,
                'unit': '吨',
                'destination_country': '日本',
                'trade_month': '2025-02'
            },
            {
                'product_name': '活、鲜或冷的螯龙虾',
                'category': '甲壳类',
                'hs_code': '03063200',
                'export_value': 98500000,
                'export_weight': 3100,
                'unit': '吨',
                'destination_country': '加拿大',
                'trade_month': '2025-02'
            },
            {
                'product_name': '龙虾制品',
                'category': '加工食品',
                'hs_code': '16053000',
                'export_value': 76500000,
                'export_weight': 2500,
                'unit': '吨',
                'destination_country': '欧盟',
                'trade_month': '2025-02'
            },
            {
                'product_name': '冻对虾',
                'category': '甲壳类',
                'hs_code': '03061612',
                'export_value': 65400000,
                'export_weight': 8200,
                'unit': '吨',
                'destination_country': '韩国',
                'trade_month': '2025-02'
            },
            {
                'product_name': '活、鲜或冷的蟹',
                'category': '甲壳类',
                'hs_code': '03063300',
                'export_value': 52800000,
                'export_weight': 4200,
                'unit': '吨',
                'destination_country': '俄罗斯',
                'trade_month': '2025-02'
            },
            {
                'product_name': '冻虾仁',
                'category': '甲壳类',
                'hs_code': '03061790',
                'export_value': 45600000,
                'export_weight': 3800,
                'unit': '吨',
                'destination_country': '越南',
                'trade_month': '2025-02'
            },
            {
                'product_name': '鲜、冷的鱿鱼',
                'category': '软体类',
                'hs_code': '03074300',
                'export_value': 38900000,
                'export_weight': 5600,
                'unit': '吨',
                'destination_country': '西班牙',
                'trade_month': '2025-02'
            },
            {
                'product_name': '干、盐制的墨鱼',
                'category': '软体类',
                'hs_code': '03074900',
                'export_value': 32500000,
                'export_weight': 2900,
                'unit': '吨',
                'destination_country': '泰国',
                'trade_month': '2025-02'
            },
            {
                'product_name': '扇贝制品',
                'category': '贝类',
                'hs_code': '03072100',
                'export_value': 29800000,
                'export_weight': 1800,
                'unit': '吨',
                'destination_country': '澳大利亚',
                'trade_month': '2025-02'
            }
        ]
        
        # 保存到数据库
        self._save_to_db(mock_data)
        
        return {
            'count': len(mock_data),
            'timestamp': datetime.now().isoformat()
        }
    
    def _save_to_db(self, data):
        """保存数据到数据库"""
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        for item in data:
            cursor.execute('''
                INSERT INTO customs_data 
                (product_name, category, hs_code, export_value, export_weight, 
                 unit, destination_country, trade_month)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                item['product_name'],
                item['category'],
                item['hs_code'],
                item['export_value'],
                item['export_weight'],
                item['unit'],
                item['destination_country'],
                item['trade_month']
            ))
        
        conn.commit()
        conn.close()
        print(f"[CustomsCrawler] Saved {len(data)} records to database")

if __name__ == '__main__':
    crawler = CustomsCrawler()
    result = crawler.crawl()
    print(f"Crawled {result['count']} customs records")
