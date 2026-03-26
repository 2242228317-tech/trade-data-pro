from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    # 数据库 - 使用环境变量
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./trade_data.db")
    
    # API 配置
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "TradeData Pro"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # 安全配置 - 必须设置
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # 管理员配置
    ADMIN_KEY: str = os.getenv("ADMIN_KEY", "trade888")
    
    # 爬虫配置
    CRAWLER_DELAY_MIN: float = 1.0
    CRAWLER_DELAY_MAX: float = 3.0
    CRAWLER_MAX_RETRY: int = 3
    
    # 分页配置
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # 前端URL（用于CORS）
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "*")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
