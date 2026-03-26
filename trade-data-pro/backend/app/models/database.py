from sqlalchemy import create_engine, Column, String, Integer, DECIMAL, DateTime, Text, ForeignKey, Boolean, Float
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func
from sqlalchemy.pool import NullPool
import uuid
import os

Base = declarative_base()

# 数据库URL - 优先使用环境变量
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite:///./trade_data.db"
)

# Render的PostgreSQL URL格式转换
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 创建引擎 - 生产环境配置
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL, 
        connect_args={"check_same_thread": False},
        poolclass=NullPool
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """初始化数据库表"""
    Base.metadata.create_all(bind=engine)

class Product(Base):
    """商品信息表"""
    __tablename__ = "products"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source = Column(String(20), nullable=False, index=True)
    category_id = Column(String(36), ForeignKey("categories.id"), nullable=True)
    name = Column(String(500), nullable=False, index=True)
    description = Column(Text)
    price_min = Column(DECIMAL(15, 4))
    price_max = Column(DECIMAL(15, 4))
    currency = Column(String(10), default='CNY')
    moq = Column(Integer, default=0)
    unit = Column(String(20))
    export_region = Column(String(500))
    hs_code = Column(String(20), index=True)
    supplier_name = Column(String(200))
    supplier_location = Column(String(100))
    image_url = Column(String(500))
    product_url = Column(String(500))
    trend = Column(String(10), default='stable')
    trend_value = Column(DECIMAL(5, 2))
    sales_volume = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    category = relationship("Category", back_populates="products")

class CustomsStat(Base):
    """海关统计数据表"""
    __tablename__ = "customs_stats"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    year = Column(Integer, nullable=False, index=True)
    month = Column(Integer, nullable=True, index=True)
    hs_code = Column(String(20), nullable=False, index=True)
    product_name = Column(String(500))
    export_value_usd = Column(DECIMAL(20, 2))
    export_quantity = Column(DECIMAL(20, 4))
    unit = Column(String(20))
    destination_country = Column(String(100), index=True)
    growth_rate_yoy = Column(DECIMAL(10, 4))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Category(Base):
    """商品分类表"""
    __tablename__ = "categories"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    parent_id = Column(String(36), ForeignKey("categories.id"), nullable=True)
    name = Column(String(200), nullable=False)
    hs_code_prefix = Column(String(20))
    icon = Column(String(100))
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    products = relationship("Product", back_populates="category")
    children = relationship("Category", backref="parent", remote_side=[id])

class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(100))
    company = Column(String(200))
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    
    role = Column(String(20), default="free")
    subscription_status = Column(String(20), default="active")
    subscription_expires_at = Column(DateTime, nullable=True)
    
    daily_query_limit = Column(Integer, default=10)
    daily_queries_used = Column(Integer, default=0)
    last_query_reset = Column(DateTime, default=func.now())
    data_months_limit = Column(Integer, default=3)
    can_export = Column(Boolean, default=False)
    can_api_access = Column(Boolean, default=False)
    
    stripe_customer_id = Column(String(255), nullable=True)
    stripe_subscription_id = Column(String(255), nullable=True)
    
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    payments = relationship("Payment", back_populates="user")

class Payment(Base):
    """支付记录表"""
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    amount = Column(Float, nullable=False)
    currency = Column(String(3), default="CNY")
    payment_method = Column(String(50))
    
    order_id = Column(String(100), unique=True, index=True)
    transaction_id = Column(String(255), nullable=True)
    
    plan = Column(String(20), nullable=False)
    duration_months = Column(Integer, default=1)
    
    status = Column(String(20), default="pending")
    paid_at = Column(DateTime, nullable=True)
    
    created_at = Column(DateTime, default=func.now())
    metadata_json = Column(Text, default="{}")
    
    user = relationship("User", back_populates="payments")

class CrawlerTask(Base):
    """爬虫任务记录表"""
    __tablename__ = "crawler_tasks"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    task_name = Column(String(200), nullable=False)
    source = Column(String(50), nullable=False)
    status = Column(String(20), default='pending')
    total_items = Column(Integer, default=0)
    success_items = Column(Integer, default=0)
    error_message = Column(Text)
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class DataUpdateLog(Base):
    """数据更新日志"""
    __tablename__ = "data_update_logs"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    table_name = Column(String(100), nullable=False)
    update_type = Column(String(50))
    record_count = Column(Integer)
    details = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
