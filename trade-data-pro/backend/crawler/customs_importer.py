"""
海关总署数据抓取 - 真实实现
数据来源: http://www.customs.gov.cn/customs/302249/zfxxgk/2799825/302274/302275/index.html
"""
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import re
import time
import os

class CustomsDataImporter:
    """海关数据导入器"""
    
    BASE_URL = "http://www.customs.gov.cn"
    
    # 主要统计页面URL
    STAT_PAGES = {
        "monthly_export": "/customs/302249/zfxxgk/2799825/302274/302275/index.html",
        "import_export_total": "/customs/302249/zfxxgk/2799825/302274/302276/index.html",
    }
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.data_dir = "data/customs"
        os.makedirs(self.data_dir, exist_ok=True)
    
    def download_excel(self, year: int, month: int) -> Optional[str]:
        """
        下载海关月度统计数据Excel文件
        
        Args:
            year: 年份，如 2024
            month: 月份，如 1-12
            
        Returns:
            下载的文件路径，失败返回None
        """
        # 海关数据通常按月度发布，URL格式示例：
        # http://www.customs.gov.cn/customs/resource/cms/2024/02/202402-export.xlsx
        
        # 构造文件名（实际需要从网页解析）
        filename = f"{year}{month:02d}_customs_export.xlsx"
        filepath = os.path.join(self.data_dir, filename)
        
        print(f"尝试下载 {year}年{month}月 海关数据...")
        
        # 先获取页面，找到下载链接
        try:
            page_url = f"{self.BASE_URL}{self.STAT_PAGES['monthly_export']}"
            response = self.session.get(page_url, timeout=30)
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找包含Excel下载链接的元素
            # 海关网站通常有类似 "2024年2月进出口商品贸易方式总值表" 的链接
            links = soup.find_all('a', href=True)
            
            excel_link = None
            for link in links:
                text = link.get_text(strip=True)
                # 匹配包含年月和"总值表"、"出口"等关键词的链接
                if f"{year}年{month}月" in text and ("总值表" in text or "出口" in text):
                    excel_link = link['href']
                    if not excel_link.startswith('http'):
                        excel_link = self.BASE_URL + excel_link
                    break
            
            if not excel_link:
                print(f"未找到 {year}年{month}月 的数据链接")
                return None
            
            # 下载Excel文件
            print(f"找到下载链接: {excel_link}")
            response = self.session.get(excel_link, timeout=60)
            
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f"✓ 下载成功: {filepath}")
                return filepath
            else:
                print(f"✗ 下载失败: HTTP {response.status_code}")
                return None
                
        except Exception as e:
            print(f"✗ 下载出错: {str(e)}")
            return None
    
    def parse_excel(self, filepath: str) -> List[Dict[str, Any]]:
        """
        解析海关Excel数据
        
        Args:
            filepath: Excel文件路径
            
        Returns:
            解析后的数据列表
        """
        print(f"解析文件: {filepath}")
        
        try:
            # 读取Excel文件
            # 海关数据通常有多个sheet，需要根据实际结构调整
            df = pd.read_excel(filepath, sheet_name=0)
            
            # 数据清洗（根据海关Excel的实际格式调整）
            # 通常前几行是表头说明，需要跳过
            # 列名可能包含：商品名称、数量、金额、同比等
            
            records = []
            
            # 遍历数据行
            for idx, row in df.iterrows():
                # 跳过表头行和空行
                if pd.isna(row.iloc[0]) or '合计' in str(row.iloc[0]):
                    continue
                
                # 构造记录（根据实际Excel结构调整字段映射）
                record = {
                    "hs_code": str(row.get('HS编码', row.get('商品编码', ''))),
                    "product_name": str(row.get('商品名称', row.get('商品', row.iloc[0]))),
                    "unit": str(row.get('计量单位', '—')),
                    "quantity": float(row.get('数量', 0)) if pd.notna(row.get('数量')) else 0,
                    "value_usd": float(row.get('金额(美元)', row.get('金额', 0))) if pd.notna(row.get('金额(美元)', row.get('金额'))) else 0,
                    "yoy_growth": float(row.get('同比%', 0)) if pd.notna(row.get('同比%')) else 0,
                    "year": datetime.now().year,
                    "month": datetime.now().month,
                }
                
                records.append(record)
            
            print(f"✓ 解析完成: {len(records)} 条记录")
            return records
            
        except Exception as e:
            print(f"✗ 解析出错: {str(e)}")
            return []
    
    def save_to_database(self, records: List[Dict[str, Any]], db_session):
        """
        将数据保存到数据库
        
        Args:
            records: 解析后的记录列表
            db_session: 数据库会话
        """
        from app.models.database import CustomsStat
        
        print(f"保存 {len(records)} 条记录到数据库...")
        
        try:
            for record in records:
                # 检查是否已存在
                existing = db_session.query(CustomsStat).filter_by(
                    hs_code=record['hs_code'],
                    year=record['year'],
                    month=record['month']
                ).first()
                
                if existing:
                    # 更新现有记录
                    existing.quantity = record['quantity']
                    existing.export_value = record['value_usd']
                    existing.growth_rate = record['yoy_growth']
                else:
                    # 创建新记录
                    stat = CustomsStat(
                        year=record['year'],
                        month=record['month'],
                        hs_code=record['hs_code'],
                        product_name=record['product_name'],
                        unit=record['unit'],
                        export_quantity=record['quantity'],
                        export_value=record['value_usd'],
                        growth_rate=record['yoy_growth']
                    )
                    db_session.add(stat)
            
            db_session.commit()
            print("✓ 保存成功")
            
        except Exception as e:
            db_session.rollback()
            print(f"✗ 保存失败: {str(e)}")
            raise
    
    def import_latest_data(self, db_session, months_back: int = 3):
        """
        导入最近几个月的数据
        
        Args:
            db_session: 数据库会话
            months_back: 回溯月份数，默认3个月
        """
        print(f"开始导入最近 {months_back} 个月的海关数据...")
        
        now = datetime.now()
        imported_count = 0
        
        for i in range(months_back):
            target_date = now - timedelta(days=i * 30)
            year = target_date.year
            month = target_date.month
            
            # 下载Excel
            filepath = self.download_excel(year, month)
            if filepath:
                # 解析数据
                records = self.parse_excel(filepath)
                if records:
                    # 保存到数据库
                    self.save_to_database(records, db_session)
                    imported_count += len(records)
                
                # 下载间隔，避免被封
                time.sleep(2)
        
        print(f"\n导入完成! 共导入 {imported_count} 条记录")
        return imported_count


# 使用示例
if __name__ == "__main__":
    # 测试导入
    from app.models.database import SessionLocal
    
    importer = CustomsDataImporter()
    db = SessionLocal()
    
    try:
        importer.import_latest_data(db, months_back=1)
    finally:
        db.close()
