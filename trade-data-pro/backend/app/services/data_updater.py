"""
数据更新服务 - 定时爬取并更新商品数据
"""
import asyncio
import json
import os
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Any
import schedule
import time as time_module

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crawler.alibaba_1688_real import Alibaba1688Crawler, ProductItem, save_products_to_json
from crawler.customs_real import RealCustomsCrawler, save_customs_data

class DataUpdateService:
    """数据更新服务"""
    
    def __init__(self, data_dir: str = None):
        if data_dir is None:
            # 默认使用前端数据目录
            self.data_dir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                'frontend', 'data'
            )
        else:
            self.data_dir = data_dir
        
        os.makedirs(self.data_dir, exist_ok=True)
        self.products_file = os.path.join(self.data_dir, 'all-products.json')
        self.customs_file = os.path.join(self.data_dir, 'customs-data.json')
        
        # 更新日志
        self.update_log = []
    
    def load_existing_products(self) -> List[Dict]:
        """加载现有商品数据"""
        if os.path.exists(self.products_file):
            with open(self.products_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    
    def merge_products(self, new_products: List[ProductItem], existing: List[Dict]) -> List[Dict]:
        """合并新旧商品数据"""
        existing_dict = {p['id']: p for p in existing}
        
        # 更新或添加新商品
        for product in new_products:
            existing_dict[product.id] = product.to_dict()
        
        # 转换回列表
        merged = list(existing_dict.values())
        
        # 按销量排序
        merged.sort(key=lambda x: x.get('sales_30d', 0), reverse=True)
        
        return merged
    
    async def update_1688_products(self, keywords: List[str] = None) -> int:
        """
        更新1688商品数据
        
        Args:
            keywords: 要爬取的关键词列表，None则使用默认列表
        
        Returns:
            新增/更新商品数量
        """
        if keywords is None:
            # 默认关键词列表 - 覆盖热门品类
            keywords = [
                # 电子产品
                "手机壳", "蓝牙耳机", "充电宝", "数据线", "充电器",
                "智能手表", "平板电脑", "键盘鼠标", "音箱",
                # 新能源
                "太阳能板", "锂电池", "储能电源", "LED灯",
                # 家居用品
                "收纳盒", "床上用品", "厨房用具", "清洁用品",
                # 纺织服装
                "T恤", "连衣裙", "运动鞋", "背包",
                # 机械设备
                "电动工具", "3D打印机", "激光切割",
                # 汽车配件
                "行车记录仪", "车载充电器", "汽车坐垫",
                # 美妆个护
                "化妆刷", "美甲灯", "电动牙刷",
                # 运动户外
                "瑜伽垫", "登山包", "帐篷",
                # 医疗器械
                "血压计", "体温计", "按摩器",
            ]
        
        print(f"\n{'='*60}")
        print(f"开始更新1688商品数据")
        print(f"关键词数量: {len(keywords)}")
        print(f"{'='*60}\n")
        
        all_new_products = []
        
        try:
            async with Alibaba1688Crawler(headless=True) as crawler:
                for i, keyword in enumerate(keywords, 1):
                    print(f"\n[{i}/{len(keywords)}] 爬取关键词: {keyword}")
                    
                    try:
                        products = await crawler.search_products(keyword, page_num=1, max_items=10)
                        all_new_products.extend(products)
                        print(f"    成功: {len(products)} 个商品")
                        
                        # 关键词间延时
                        if i < len(keywords):
                            await asyncio.sleep(3)
                            
                    except Exception as e:
                        print(f"    失败: {e}")
                        continue
        
        except Exception as e:
            print(f"爬虫初始化失败: {e}")
            return 0
        
        if not all_new_products:
            print("没有获取到新数据")
            return 0
        
        # 加载现有数据并合并
        existing = self.load_existing_products()
        print(f"\n现有商品: {len(existing)} 个")
        print(f"新爬取商品: {len(all_new_products)} 个")
        
        merged = self.merge_products(all_new_products, existing)
        
        # 保存
        save_products_to_json(merged, self.products_file)
        
        # 记录更新日志
        self.update_log.append({
            "timestamp": datetime.now().isoformat(),
            "type": "1688_products",
            "keywords_crawled": len(keywords),
            "new_products": len(all_new_products),
            "total_products": len(merged)
        })
        
        print(f"\n{'='*60}")
        print(f"更新完成! 总商品数: {len(merged)}")
        print(f"{'='*60}")
        
        return len(all_new_products)
    
    def update_customs_data(self) -> bool:
        """更新海关数据"""
        print(f"\n{'='*60}")
        print(f"开始更新海关数据")
        print(f"{'='*60}\n")
        
        try:
            crawler = RealCustomsCrawler()
            
            # 获取商品数据
            products = crawler.generate_sample_customs_data()
            save_customs_data(products, self.customs_file)
            
            # 获取国别数据（可以分开存储）
            countries = crawler.get_country_trade_data()
            countries_file = os.path.join(self.data_dir, 'customs-countries.json')
            save_customs_data(countries, countries_file)
            
            print(f"海关商品数据: {len(products)} 条")
            print(f"海关国别数据: {len(countries)} 条")
            
            # 记录日志
            self.update_log.append({
                "timestamp": datetime.now().isoformat(),
                "type": "customs_data",
                "products_count": len(products),
                "countries_count": len(countries)
            })
            
            print(f"\n{'='*60}")
            print(f"海关数据更新完成!")
            print(f"{'='*60}")
            
            return True
            
        except Exception as e:
            print(f"更新海关数据失败: {e}")
            return False
    
    def get_update_summary(self) -> Dict[str, Any]:
        """获取更新摘要"""
        products = self.load_existing_products()
        
        # 统计品类分布
        categories = {}
        for p in products:
            cat = p.get('category', '未知')
            categories[cat] = categories.get(cat, 0) + 1
        
        # 统计趋势
        trends = {'up': 0, 'down': 0, 'stable': 0}
        for p in products:
            trend = p.get('trend', 'stable')
            trends[trend] = trends.get(trend, 0) + 1
        
        return {
            "total_products": len(products),
            "categories": categories,
            "trends": trends,
            "last_update": self.update_log[-1] if self.update_log else None,
            "update_history": self.update_log[-10:]  # 最近10次
        }
    
    def print_summary(self):
        """打印数据摘要"""
        summary = self.get_update_summary()
        
        print(f"\n{'='*60}")
        print(f"数据摘要")
        print(f"{'='*60}")
        print(f"总商品数: {summary['total_products']}")
        print(f"\n品类分布:")
        for cat, count in sorted(summary['categories'].items(), key=lambda x: -x[1])[:10]:
            print(f"  {cat}: {count} 个")
        print(f"\n趋势分布:")
        for trend, count in summary['trends'].items():
            print(f"  {trend}: {count} 个")
        print(f"{'='*60}\n")

# 定时任务
def run_scheduled_update():
    """运行定时更新"""
    service = DataUpdateService()
    
    # 定义更新任务
    def job_update_1688():
        print(f"\n[定时任务] {datetime.now()} 开始更新1688数据")
        asyncio.run(service.update_1688_products())
        service.print_summary()
    
    def job_update_customs():
        print(f"\n[定时任务] {datetime.now()} 开始更新海关数据")
        service.update_customs_data()
    
    # 设置定时任务
    # 每天凌晨2点更新1688数据
    schedule.every().day.at("02:00").do(job_update_1688)
    
    # 每周一更新海关数据
    schedule.every().monday.at("03:00").do(job_update_customs)
    
    print("定时任务已启动:")
    print("  - 每天 02:00 更新1688商品数据")
    print("  - 每周一 03:00 更新海关数据")
    print("\n按 Ctrl+C 停止\n")
    
    # 运行调度循环
    while True:
        schedule.run_pending()
        time_module.sleep(60)

async def run_single_update(keywords: List[str] = None):
    """运行单次更新（用于测试）"""
    service = DataUpdateService()
    
    # 更新1688数据
    count = await service.update_1688_products(keywords)
    
    # 更新海关数据
    service.update_customs_data()
    
    # 打印摘要
    service.print_summary()
    
    return count

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='数据更新服务')
    parser.add_argument('--scheduled', action='store_true', help='运行定时任务模式')
    parser.add_argument('--keywords', nargs='+', help='指定关键词列表')
    parser.add_argument('--test', action='store_true', help='测试模式（只爬取少量数据）')
    
    args = parser.parse_args()
    
    if args.scheduled:
        # 定时任务模式
        run_scheduled_update()
    elif args.test:
        # 测试模式 - 只爬取少量数据
        test_keywords = ["手机壳", "蓝牙耳机"]
        asyncio.run(run_single_update(test_keywords))
    else:
        # 单次更新模式
        asyncio.run(run_single_update(args.keywords))
