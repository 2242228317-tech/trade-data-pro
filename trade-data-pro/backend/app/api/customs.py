from fastapi import APIRouter, Query
from typing import List, Optional
from pydantic import BaseModel
from decimal import Decimal
import json
import os

router = APIRouter()

# 加载海关数据
def load_customs_data():
    """加载海关数据"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(current_dir, '..', '..', '..', 'frontend', 'data', 'customs-data.json')
    
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def load_country_data():
    """加载国别数据"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_file = os.path.join(current_dir, '..', '..', '..', 'frontend', 'data', 'customs-countries.json')
    
    if os.path.exists(data_file):
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# API路由
@router.get("/")
async def get_customs_data(
    year: Optional[int] = None,
    month: Optional[int] = None,
    hs_code: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    """获取海关商品统计数据"""
    data = load_customs_data()
    
    # 过滤
    if year:
        data = [d for d in data if d.get('year') == year]
    if month:
        data = [d for d in data if d.get('month') == month]
    if hs_code:
        data = [d for d in data if d.get('hs_code', '').startswith(hs_code)]
    
    # 分页
    total = len(data)
    start = (page - 1) * page_size
    end = start + page_size
    paginated = data[start:end]
    
    return {
        "success": True,
        "data": paginated,
        "total": total,
        "page": page,
        "page_size": page_size
    }

@router.get("/countries")
async def get_country_data(
    year: Optional[int] = None,
    limit: int = Query(10, ge=1, le=50)
):
    """获取国别贸易数据"""
    data = load_country_data()
    
    # 默认返回前N个
    result = data[:limit]
    
    return {
        "success": True,
        "data": result
    }

@router.get("/summary")
async def get_summary(year: Optional[int] = None):
    """获取汇总统计"""
    data = load_customs_data()
    
    total_export = sum(d.get('value_usd', 0) for d in data)
    total_categories = len(set(d.get('hs_code', '') for d in data))
    
    return {
        "success": True,
        "data": {
            "total_export_value": round(total_export / 100000000, 2),  # 亿美元
            "total_categories": total_categories,
            "total_records": len(data)
        }
    }

@router.get("/hs-codes")
async def get_hs_codes():
    """获取HS编码列表"""
    hs_codes = [
        {"code": "01", "name": "活动物", "level": 1},
        {"code": "84", "name": "核反应堆、锅炉、机械器具", "level": 1},
        {"code": "85", "name": "电机、电气设备及其零件", "level": 1},
        {"code": "8517", "name": "电话机", "level": 2, "parent": "85"},
        {"code": "8471", "name": "计算机及部件", "level": 2, "parent": "84"},
        {"code": "8528", "name": "电视及显示器", "level": 2, "parent": "85"},
        {"code": "8541", "name": "集成电路", "level": 2, "parent": "85"},
    ]
    
    return {
        "success": True,
        "data": hs_codes
    }
