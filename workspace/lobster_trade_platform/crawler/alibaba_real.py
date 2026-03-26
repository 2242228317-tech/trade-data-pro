"""
阿里巴巴国际站真实爬虫
使用 Selenium 模拟浏览器访问
"""

import os
import sys
import time
import random
import sqlite3
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent

DATABASE = 'database/trade_data.db'

class AlibabaRealCrawler:
    """阿里巴巴国际站真实爬虫"""
    
    def __init__(self):
        self.ua = UserAgent()
        self.driver = None
        
    def _init_driver(self):
        """初始化浏览器驱动"""
        chrome_options = Options()
        
        # 反爬设置
        chrome_options.add_argument(f'--user-agent={self.ua.random}')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # 无头模式（后台运行）
        # chrome_options.add_argument('--headless')
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
            })
            self.driver.set_page_load_timeout(30)
            print("[Selenium] Chrome driver initialized")
        except Exception as e:
            print(f"[Error] Failed to init driver: {e}")
            raise
    
    def crawl(self, keyword='lobster', pages=2):
        """
        爬取阿里巴巴国际站产品数据
        """
        print(f"[AlibabaRealCrawler] Starting crawl for: {keyword}")
        
        if not self.driver:
            self._init_driver()
        
        products = []
        
        try:
            for page in range(1, pages + 1):
                print(f"[Crawling] Page {page}/{pages}")
                
                # 构建搜索URL
                url = f"https://www.alibaba.com/trade/search?SearchText={keyword}&page={page}"
                
                self.driver.get(url)
                time.sleep(random.uniform(3, 5))  # 随机延迟
                
                # 等待产品加载
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-spm="1000000"]'))
                    )
                except:
                    print(f"[Warning] Timeout waiting for products on page {page}")
                    continue
                
                # 获取产品列表
                product_cards = self.driver.find_elements(By.CSS_SELECTOR, '.J-offer-wrapper')
                
                print(f"[Found] {len(product_cards)} products on page {page}")
                
                for card in product_cards[:10]:  # 每页取前10个
                    try:
                        product = self._parse_product(card)
                        if product:
                            products.append(product)
                    except Exception as e:
                        print(f"[Parse Error] {e}")
                        continue
                
                # 随机延迟，避免被封
                time.sleep(random.uniform(2, 4))
        
        except Exception as e:
            print(f"[Crawl Error] {e}")
        
        finally:
            if self.driver:
                self.driver.quit()
                print("[Selenium] Driver closed")
        
        # 保存到数据库
        if products:
            self._save_to_db(products)
        
        return {
            'count': len(products),
            'keyword': keyword,
            'timestamp': datetime.now().isoformat()
        }
    
    def _parse_product(self, card):
        """解析单个产品卡片"""
        try:
            # 产品名称
            try:
                name = card.find_element(By.CSS_SELECTOR, '.elements-title-normal').text
            except:
                name = 'Unknown Product'
            
            # 价格
            try:
                price_text = card.find_element(By.CSS_SELECTOR, '.elements-offer-price-normal').text
                # 提取数字
                import re
                price_match = re.search(r'[\d,]+\.?\d*', price_text.replace(',', ''))
                price = float(price_match.group()) if price_match else 0
                currency = 'USD'
            except:
                price = 0
                currency = 'USD'
            
            # 供应商
            try:
                supplier = card.find_element(By.CSS_SELECTOR, '.elements-company-name').text
            except:
                supplier = 'Unknown Supplier'
            
            # 起订量
            try:
                moq = card.find_element(By.CSS_SELECTOR, '.element-offer-min-order-normal').text
            except:
                moq = 'Contact Supplier'
            
            # 链接
            try:
                link = card.find_element(By.TAG_NAME, 'a').get_attribute('href')
            except:
                link = ''
            
            # 模拟销售额（实际无法获取）
            estimated_sales = random.randint(100, 2000)
            revenue = price * estimated_sales
            
            return {
                'product_name': name,
                'price': price,
                'currency': currency,
                'min_order': moq,
                'supplier': supplier,
                'location': 'International',
                'sales_count': estimated_sales,
                'revenue_estimate': revenue,
                'product_url': link,
                'image_url': ''
            }
        
        except Exception as e:
            print(f"[Parse Error] {e}")
            return None
    
    def _save_to_db(self, data):
        """保存数据到数据库"""
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        for item in data:
            cursor.execute('''
                INSERT INTO alibaba_products 
                (product_name, price, currency, min_order, supplier, location, 
                 sales_count, revenue_estimate, product_url, image_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                item['product_name'],
                item['price'],
                item['currency'],
                item['min_order'],
                item['supplier'],
                item['location'],
                item['sales_count'],
                item['revenue_estimate'],
                item['product_url'],
                item['image_url']
            ))
        
        conn.commit()
        conn.close()
        print(f"[AlibabaRealCrawler] Saved {len(data)} records to database")

if __name__ == '__main__':
    crawler = AlibabaRealCrawler()
    result = crawler.crawl('lobster', pages=2)
    print(f"Crawled {result['count']} products")
