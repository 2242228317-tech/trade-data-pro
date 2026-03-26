from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any
from decimal import Decimal

router = APIRouter()

class DashboardOverview(BaseModel):
    total_products: int
    today_new_products: int
    total_export_value: Decimal
    monthly_growth: Decimal
    top_export_regions: List[Dict[str, Any]]
    hot_categories: List[Dict[str, Any]]

class ChartData(BaseModel):
    labels: List[str]
    datasets: List[Dict[str, Any]]

@router.get("/overview", response_model=DashboardOverview)
async def get_overview():
    """获取仪表盘概览数据"""
    # TODO: 从数据库获取实时数据
    return {
        "total_products": 0,
        "today_new_products": 0,
        "total_export_value": Decimal("0"),
        "monthly_growth": Decimal("0"),
        "top_export_regions": [
            {"name": "美国", "value": 35, "amount": "120.5B"},
            {"name": "欧盟", "value": 28, "amount": "98.3B"},
            {"name": "东盟", "value": 18, "amount": "62.1B"},
            {"name": "日本", "value": 10, "amount": "34.7B"},
            {"name": "韩国", "value": 9, "amount": "28.9B"},
        ],
        "hot_categories": [
            {"name": "电子产品", "growth": 15.2, "trend": "up"},
            {"name": "机械设备", "growth": 8.7, "trend": "up"},
            {"name": "纺织服装", "growth": -2.3, "trend": "down"},
            {"name": "化工产品", "growth": 5.1, "trend": "up"},
        ]
    }

@router.get("/trends", response_model=ChartData)
async def get_trends(days: int = 30):
    """获取出口趋势数据"""
    # TODO: 从数据库获取趋势数据
    return {
        "labels": ["2024-01", "2024-02", "2024-03", "2024-04", "2024-05", "2024-06"],
        "datasets": [
            {
                "label": "出口金额 (亿美元)",
                "data": [280.5, 265.3, 298.7, 312.4, 305.8, 320.1],
                "borderColor": "#10b981",
                "backgroundColor": "rgba(16, 185, 129, 0.1)",
            }
        ]
    }

@router.get("/category-distribution")
async def get_category_distribution():
    """获取品类分布数据"""
    return {
        "labels": ["电子产品", "机械设备", "纺织服装", "化工产品", "农产品", "其他"],
        "datasets": [{
            "data": [35, 25, 15, 12, 8, 5],
            "backgroundColor": [
                "#3b82f6", "#10b981", "#f59e0b", 
                "#ef4444", "#8b5cf6", "#6b7280"
            ]
        }]
    }

@router.get("/realtime-updates")
async def get_realtime_updates(limit: int = 10):
    """获取实时更新数据"""
    # TODO: 从数据库获取最新更新的产品
    return {
        "updates": [
            {"time": "10分钟前", "action": "新增产品", "detail": "智能手机出口数据更新"},
            {"time": "25分钟前", "action": "价格变动", "detail": "锂电池出口价格上涨 5%"},
            {"time": "1小时前", "action": "数据导入", "detail": "3月海关数据已同步"},
        ]
    }

@router.get("/rankings")
async def get_rankings(type: str = "product", limit: int = 10):
    """获取排行榜数据
    
    type: product | country | category
    """
    if type == "product":
        return {
            "rankings": [
                {"rank": 1, "name": "智能手机", "value": "45.2B", "change": "+12%"},
                {"rank": 2, "name": "笔记本电脑", "value": "38.7B", "change": "+8%"},
                {"rank": 3, "name": "集成电路", "value": "32.1B", "change": "+15%"},
            ]
        }
    elif type == "country":
        return {
            "rankings": [
                {"rank": 1, "name": "美国", "value": "524.4B", "change": "-2.3%"},
                {"rank": 2, "name": "日本", "value": "157.4B", "change": "+1.2%"},
                {"rank": 3, "name": "韩国", "value": "148.9B", "change": "+3.5%"},
            ]
        }
    return {"rankings": []}
