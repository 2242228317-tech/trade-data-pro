#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据初始化脚本
运行: python init_data.py
"""
import json
import sys
import os

# 添加backend到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.models.database import init_db, SessionLocal, Product, Category, CustomsStat

def init_categories():
    """初始化商品分类"""
    categories = [
        {"id": "cat_001", "name": "电子产品", "hs_code_prefix": "85", "icon": "📱", "sort_order": 1},
        {"id": "cat_002", "name": "家居用品", "hs_code_prefix": "94", "icon": "🏠", "sort_order": 2},
        {"id": "cat_003", "name": "纺织服装", "hs_code_prefix": "61-63", "icon": "👕", "sort_order": 3},
        {"id": "cat_004", "name": "机械设备", "hs_code_prefix": "84", "icon": "⚙️", "sort_order": 4},
        {"id": "cat_005", "name": "化工产品", "hs_code_prefix": "28-38", "icon": "🧪", "sort_order": 5},
        {"id": "cat_006", "name": "新能源", "hs_code_prefix": "85", "icon": "🔋", "sort_order": 6},
        {"id": "cat_007", "name": "运动户外", "hs_code_prefix": "95", "icon": "⚽", "sort_order": 7},
        {"id": "cat_008", "name": "玩具礼品", "hs_code_prefix": "95", "icon": "🎁", "sort_order": 8},
        {"id": "cat_009", "name": "汽车配件", "hs_code_prefix": "87", "icon": "🚗", "sort_order": 9},
        {"id": "cat_010", "name": "医疗器械", "hs_code_prefix": "90", "icon": "🏥", "sort_order": 10},
    ]
    
    db = SessionLocal()
    try:
        for cat_data in categories:
            existing = db.query(Category).filter(Category.id == cat_data["id"]).first()
            if not existing:
                category = Category(**cat_data)
                db.add(category)
        db.commit()
        print(f"✅ 分类初始化完成: {len(categories)}个")
    finally:
        db.close()

def init_sample_products():
    """初始化示例产品数据"""
    products = [
        # 电子产品
        {
            "id": "prod_001", "source": "1688", "category_id": "cat_001",
            "name": "智能手机充电器 65W快充", "description": "氮化镓技术，支持多协议快充",
            "price_min": 25.00, "price_max": 45.00, "moq": 100, "unit": "个",
            "supplier_location": "深圳", "trend": "up", "trend_value": 15.5,
            "sales_volume": 50000, "hs_code": "85044099"
        },
        {
            "id": "prod_002", "source": "1688", "category_id": "cat_001",
            "name": "无线蓝牙耳机 TWS", "description": "主动降噪，长续航",
            "price_min": 35.00, "price_max": 80.00, "moq": 50, "unit": "个",
            "supplier_location": "东莞", "trend": "up", "trend_value": 22.3,
            "sales_volume": 80000, "hs_code": "85183000"
        },
        {
            "id": "prod_003", "source": "1688", "category_id": "cat_001",
            "name": "便携投影仪 1080P", "description": "家用高清，智能系统",
            "price_min": 280.00, "price_max": 450.00, "moq": 20, "unit": "台",
            "supplier_location": "深圳", "trend": "stable", "trend_value": 5.2,
            "sales_volume": 15000, "hs_code": "85286910"
        },
        # 新能源
        {
            "id": "prod_004", "source": "1688", "category_id": "cat_006",
            "name": "太阳能电池板 100W", "description": "单晶硅，高效率转换",
            "price_min": 120.00, "price_max": 180.00, "moq": 10, "unit": "块",
            "supplier_location": "无锡", "trend": "up", "trend_value": 45.8,
            "sales_volume": 25000, "hs_code": "85414020"
        },
        {
            "id": "prod_005", "source": "1688", "category_id": "cat_006",
            "name": "储能电源 500Wh", "description": "户外应急，多接口输出",
            "price_min": 350.00, "price_max": 550.00, "moq": 10, "unit": "台",
            "supplier_location": "深圳", "trend": "up", "trend_value": 38.2,
            "sales_volume": 12000, "hs_code": "85044099"
        },
        # 家居用品
        {
            "id": "prod_006", "source": "1688", "category_id": "cat_002",
            "name": "智能LED台灯", "description": "护眼可调光，USB充电",
            "price_min": 18.00, "price_max": 35.00, "moq": 100, "unit": "个",
            "supplier_location": "中山", "trend": "stable", "trend_value": 8.5,
            "sales_volume": 60000, "hs_code": "94052000"
        },
        {
            "id": "prod_007", "source": "1688", "category_id": "cat_002",
            "name": "厨房收纳套装", "description": "多层设计，节省空间",
            "price_min": 15.00, "price_max": 28.00, "moq": 200, "unit": "套",
            "supplier_location": "义乌", "trend": "up", "trend_value": 12.3,
            "sales_volume": 45000, "hs_code": "39241000"
        },
        # 纺织服装
        {
            "id": "prod_008", "source": "1688", "category_id": "cat_003",
            "name": "运动速干T恤", "description": "透气排汗，多色可选",
            "price_min": 12.00, "price_max": 22.00, "moq": 300, "unit": "件",
            "supplier_location": "泉州", "trend": "stable", "trend_value": 6.8,
            "sales_volume": 100000, "hs_code": "61091000"
        },
        {
            "id": "prod_009", "source": "1688", "category_id": "cat_003",
            "name": "瑜伽服套装", "description": "高弹面料，塑形修身",
            "price_min": 35.00, "price_max": 55.00, "moq": 100, "unit": "套",
            "supplier_location": "广州", "trend": "up", "trend_value": 18.5,
            "sales_volume": 35000, "hs_code": "61143000"
        },
        # 运动户外
        {
            "id": "prod_010", "source": "1688", "category_id": "cat_007",
            "name": "露营帐篷 3-4人", "description": "防水防晒，快速搭建",
            "price_min": 120.00, "price_max": 200.00, "moq": 30, "unit": "顶",
            "supplier_location": "宁波", "trend": "up", "trend_value": 32.6,
            "sales_volume": 18000, "hs_code": "63062200"
        },
        {
            "id": "prod_011", "source": "1688", "category_id": "cat_007",
            "name": "折叠自行车 20寸", "description": "轻便便携，变速系统",
            "price_min": 180.00, "price_max": 320.00, "moq": 15, "unit": "辆",
            "supplier_location": "天津", "trend": "stable", "trend_value": 4.2,
            "sales_volume": 8000, "hs_code": "87120089"
        },
        # 玩具礼品
        {
            "id": "prod_012", "source": "1688", "category_id": "cat_008",
            "name": "益智积木套装", "description": "兼容乐高，多种造型",
            "price_min": 25.00, "price_max": 60.00, "moq": 100, "unit": "盒",
            "supplier_location": "汕头", "trend": "stable", "trend_value": 7.5,
            "sales_volume": 40000, "hs_code": "95030089"
        },
        # 汽车配件
        {
            "id": "prod_013", "source": "1688", "category_id": "cat_009",
            "name": "车载手机支架", "description": "磁吸设计，稳固不晃",
            "price_min": 8.00, "price_max": 18.00, "moq": 500, "unit": "个",
            "supplier_location": "深圳", "trend": "stable", "trend_value": 5.8,
            "sales_volume": 120000, "hs_code": "87082990"
        },
        # 医疗器械
        {
            "id": "prod_014", "source": "1688", "category_id": "cat_010",
            "name": "电子血压计", "description": "臂式测量，语音播报",
            "price_min": 45.00, "price_max": 85.00, "moq": 50, "unit": "台",
            "supplier_location": "深圳", "trend": "up", "trend_value": 15.2,
            "sales_volume": 22000, "hs_code": "90189020"
        },
    ]
    
    db = SessionLocal()
    try:
        for prod_data in products:
            existing = db.query(Product).filter(Product.id == prod_data["id"]).first()
            if not existing:
                product = Product(**prod_data)
                db.add(product)
        db.commit()
        print(f"✅ 产品初始化完成: {len(products)}个")
    finally:
        db.close()

def init_customs_data():
    """初始化海关统计数据"""
    customs_data = [
        {"year": 2024, "month": 1, "hs_code": "850440", "product_name": "静态变流器", "export_value_usd": 2850000000, "destination_country": "美国", "growth_rate_yoy": 0.125},
        {"year": 2024, "month": 1, "hs_code": "851830", "product_name": "耳机", "export_value_usd": 1200000000, "destination_country": "美国", "growth_rate_yoy": 0.085},
        {"year": 2024, "month": 1, "hs_code": "854140", "product_name": "太阳能电池", "export_value_usd": 980000000, "destination_country": "荷兰", "growth_rate_yoy": 0.458},
        {"year": 2024, "month": 2, "hs_code": "850440", "product_name": "静态变流器", "export_value_usd": 2680000000, "destination_country": "美国", "growth_rate_yoy": 0.098},
        {"year": 2024, "month": 2, "hs_code": "851830", "product_name": "耳机", "export_value_usd": 1150000000, "destination_country": "美国", "growth_rate_yoy": 0.072},
        {"year": 2024, "month": 2, "hs_code": "854140", "product_name": "太阳能电池", "export_value_usd": 920000000, "destination_country": "德国", "growth_rate_yoy": 0.412},
        {"year": 2024, "month": 3, "hs_code": "610910", "product_name": "棉制T恤", "export_value_usd": 850000000, "destination_country": "日本", "growth_rate_yoy": 0.065},
        {"year": 2024, "month": 3, "hs_code": "950300", "product_name": "玩具", "export_value_usd": 720000000, "destination_country": "美国", "growth_rate_yoy": 0.042},
    ]
    
    db = SessionLocal()
    try:
        count = 0
        for data in customs_data:
            existing = db.query(CustomsStat).filter(
                CustomsStat.hs_code == data["hs_code"],
                CustomsStat.year == data["year"],
                CustomsStat.month == data["month"]
            ).first()
            if not existing:
                stat = CustomsStat(**data)
                db.add(stat)
                count += 1
        db.commit()
        print(f"✅ 海关数据初始化完成: {count}条")
    finally:
        db.close()

def main():
    print("🚀 开始初始化数据...")
    print("=" * 50)
    
    # 初始化数据库表
    print("📊 创建数据库表...")
    init_db()
    print("✅ 数据库表创建完成\n")
    
    # 初始化数据
    init_categories()
    init_sample_products()
    init_customs_data()
    
    print("=" * 50)
    print("🎉 数据初始化完成！")
    print("\n你可以通过以下地址访问：")
    print("- 前端: http://localhost:3000")
    print("- 后端API: http://localhost:8000")
    print("- API文档: http://localhost:8000/docs")

if __name__ == "__main__":
    main()
