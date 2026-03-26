from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import date
import json
import os

router = APIRouter()

# 统一响应模型
class ApiResponse(BaseModel):
    success: bool = True
    data: Optional[dict] = None
    error: Optional[str] = None

# 加载商品数据
def load_products():
    """从前端数据目录加载商品数据"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    possible_paths = [
        os.path.join(current_dir, '..', '..', '..', 'frontend', 'data', 'all-products.json'),
        os.path.join(current_dir, '..', '..', 'frontend', 'data', 'all-products.json'),
        r'C:\Users\22422\.openclaw\workspace\trade-data-pro\frontend\data\all-products.json',
    ]
    
    for path in possible_paths:
        abs_path = os.path.abspath(path)
        if os.path.exists(abs_path):
            with open(abs_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
    
    return []

# 全局商品数据
PRODUCTS_DATA = load_products()

# Pydantic 模型
class PriceRange(BaseModel):
    min: float
    max: float
    currency: str
    unit: str

class Supplier(BaseModel):
    name: str
    location: str
    rating: float
    yearsInBusiness: int
    verified: bool

class ProductResponse(BaseModel):
    id: str
    name: str
    description: str
    category: str
    subcategory: str
    price: PriceRange
    moq: int
    supplier: Supplier
    images: List[str]
    specifications: dict
    rating: float
    reviewCount: int
    salesVolume: int
    trend: str
    trendValue: float
    region: str

class ProductListData(BaseModel):
    total: int
    items: List[dict]
    page: int
    page_size: int

# 商品 API
@router.get("/")
async def get_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    keyword: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    export_region: Optional[str] = None,
    sort_by: str = Query("salesVolume", pattern="^(price|salesVolume|trendValue|rating|reviewCount)$"),
    sort_order: str = Query("desc", pattern="^(asc|desc)$")
):
    """获取商品列表"""
    products = PRODUCTS_DATA.copy()
    
    # 筛选
    if category and category != '全部':
        products = [p for p in products if p.get('category') == category]
    
    if keyword:
        products = [p for p in products if keyword.lower() in p.get('name', '').lower() or 
                    keyword.lower() in p.get('description', '').lower()]
    
    if min_price is not None:
        products = [p for p in products if p.get('price', {}).get('min', 0) >= min_price]
    
    if max_price is not None:
        products = [p for p in products if p.get('price', {}).get('max', 999999) <= max_price]
    
    # 排序
    reverse = sort_order == 'desc'
    if sort_by == 'price':
        products.sort(key=lambda x: x.get('price', {}).get('min', 0), reverse=reverse)
    elif sort_by == 'salesVolume':
        products.sort(key=lambda x: x.get('salesVolume', 0), reverse=reverse)
    elif sort_by == 'trendValue':
        products.sort(key=lambda x: x.get('trendValue', 0), reverse=reverse)
    elif sort_by == 'rating':
        products.sort(key=lambda x: x.get('rating', 0), reverse=reverse)
    elif sort_by == 'reviewCount':
        products.sort(key=lambda x: x.get('reviewCount', 0), reverse=reverse)
    
    # 分页
    total = len(products)
    start = (page - 1) * page_size
    end = start + page_size
    paginated_products = products[start:end]
    
    return {
        "success": True,
        "data": {
            "total": total,
            "items": paginated_products,
            "page": page,
            "page_size": page_size
        }
    }

@router.get("/{product_id}")
async def get_product(product_id: str):
    """获取商品详情"""
    for product in PRODUCTS_DATA:
        if product.get('id') == product_id:
            return {
                "success": True,
                "data": product
            }
    
    raise HTTPException(status_code=404, detail="Product not found")

@router.get("/trending")
async def get_trending_products(limit: int = Query(10, ge=1, le=50)):
    """获取热门商品"""
    sorted_products = sorted(PRODUCTS_DATA, key=lambda x: x.get('salesVolume', 0), reverse=True)
    return {
        "success": True,
        "data": sorted_products[:limit]
    }

@router.get("/filters")
async def get_filter_options():
    """获取筛选选项"""
    categories = list(set(p.get('category') for p in PRODUCTS_DATA if p.get('category')))
    subcategories = list(set(p.get('subcategory') for p in PRODUCTS_DATA if p.get('subcategory')))
    regions = list(set(p.get('region') for p in PRODUCTS_DATA if p.get('region')))
    
    return {
        "success": True,
        "data": {
            "categories": sorted(categories),
            "subcategories": sorted(subcategories),
            "regions": sorted(regions)
        }
    }

@router.get("/stats/trends")
async def get_price_trends(
    product_id: Optional[str] = None,
    category_id: Optional[str] = None,
    days: int = Query(30, ge=7, le=365)
):
    """获取价格趋势"""
    return {
        "success": True,
        "data": {
            "trends": [
                {"date": "2024-01", "price": 100, "volume": 1000},
                {"date": "2024-02", "price": 105, "volume": 1200},
                {"date": "2024-03", "price": 102, "volume": 1100},
            ]
        }
    }

@router.get("/stats/regions")
async def get_export_regions(
    category: Optional[str] = None,
    min_quantity: Optional[int] = None
):
    """获取出口地区分布"""
    return {
        "success": True,
        "data": {
            "regions": [
                {"name": "美国", "value": 35},
                {"name": "欧盟", "value": 28},
                {"name": "东盟", "value": 20},
                {"name": "日本", "value": 10},
                {"name": "其他", "value": 7},
            ]
        }
    }

@router.post("/compare")
async def compare_products(ids: List[str]):
    """对比多个商品"""
    products = [p for p in PRODUCTS_DATA if p.get('id') in ids]
    return {
        "success": True,
        "data": products
    }
