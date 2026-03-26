"""
会员系统数据库模型
"""
from datetime import datetime, timedelta
from enum import Enum
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, JSON, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship
from app.models.database import Base

class UserRole(str, Enum):
    """用户角色"""
    FREE = "free"           # 免费用户
    BASIC = "basic"         # 基础会员
    PRO = "pro"             # 专业会员
    ENTERPRISE = "enterprise"  # 企业会员

class SubscriptionStatus(str, Enum):
    """订阅状态"""
    ACTIVE = "active"       # 生效中
    EXPIRED = "expired"     # 已过期
    CANCELLED = "cancelled" # 已取消
    PENDING = "pending"     # 待支付

class User(Base):
    """用户表 - 扩展现有模型"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # 会员信息
    role = Column(String(20), default="free")
    subscription_status = Column(String(20), default="active")
    subscription_expires_at = Column(DateTime, nullable=True)  # 会员到期时间
    
    # 配额限制（每日重置）
    daily_query_limit = Column(Integer, default=10)   # 每日查询次数限制
    daily_queries_used = Column(Integer, default=0)   # 今日已用
    last_query_reset = Column(DateTime, default=datetime.utcnow)  # 上次重置时间
    
    # 数据访问范围
    data_months_limit = Column(Integer, default=3)    # 可看最近几个月数据
    can_export = Column(Boolean, default=False)       # 是否可导出
    can_api_access = Column(Boolean, default=False)   # 是否可用API
    
    # 支付相关
    stripe_customer_id = Column(String(255), nullable=True)  # Stripe客户ID
    stripe_subscription_id = Column(String(255), nullable=True)
    
    # 元数据
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    payments = relationship("Payment", back_populates="user")

class Payment(Base):
    """支付记录表"""
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 支付信息
    amount = Column(Float, nullable=False)            # 金额
    currency = Column(String(3), default="CNY")       # 币种
    payment_method = Column(String(50))               # 支付方式: alipay/wechat/stripe
    
    # 订单信息
    order_id = Column(String(100), unique=True, index=True)  # 商户订单号
    transaction_id = Column(String(255), nullable=True)      # 第三方支付流水号
    
    # 订阅信息
    plan = Column(String(20), nullable=False)  # 购买的套餐
    duration_months = Column(Integer, default=1)      # 订阅时长(月)
    
    # 状态
    status = Column(String(20), default="pending")    # pending/paid/failed/refunded
    paid_at = Column(DateTime, nullable=True)
    
    # 元数据
    created_at = Column(DateTime, default=datetime.utcnow)
    metadata_json = Column(Text, default="{}")             # 扩展字段(JSON字符串)
    
    user = relationship("User", back_populates="payments")

# 会员配置（代码中定义，也可放数据库）
MEMBERSHIP_PLANS = {
    UserRole.FREE: {
        "name": "免费版",
        "price_cny": 0,
        "price_usd": 0,
        "daily_queries": 10,
        "data_months": 3,
        "can_export": False,
        "can_api": False,
        "description": "适合个人体验"
    },
    UserRole.BASIC: {
        "name": "基础版",
        "price_cny": 29,
        "price_usd": 4.99,
        "daily_queries": 100,
        "data_months": 12,
        "can_export": True,
        "can_api": False,
        "description": "适合个人研究者"
    },
    UserRole.PRO: {
        "name": "专业版",
        "price_cny": 99,
        "price_usd": 14.99,
        "daily_queries": 999999,  # 实际上不限
        "data_months": 60,        # 5年
        "can_export": True,
        "can_api": True,
        "description": "适合专业分析师"
    },
    UserRole.ENTERPRISE: {
        "name": "企业版",
        "price_cny": 299,
        "price_usd": 49.99,
        "daily_queries": 999999,
        "data_months": 120,       # 10年
        "can_export": True,
        "can_api": True,
        "description": "适合企业数据部门"
    }
}
