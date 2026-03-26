from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api import products, customs, dashboard, crawler, auth, manual_payment
from app.models.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时
    print("🚀 TradeData Pro starting...")
    try:
        init_db()
        print("✅ Database initialized")
    except Exception as e:
        print(f"⚠️ Database init warning: {e}")
    yield
    # 关闭时
    print("👋 TradeData Pro shutting down...")

def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME,
        description="中国出口商品数据分析平台",
        version="1.0.0",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
    )
    
    # CORS 配置
    allow_origins = [settings.FRONTEND_URL] if settings.FRONTEND_URL != "*" else ["*"]
    application.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # 注册路由
    application.include_router(
        products.router,
        prefix=f"{settings.API_V1_STR}/products",
        tags=["products"]
    )
    application.include_router(
        customs.router,
        prefix=f"{settings.API_V1_STR}/customs",
        tags=["customs"]
    )
    application.include_router(
        dashboard.router,
        prefix=f"{settings.API_V1_STR}/dashboard",
        tags=["dashboard"]
    )
    application.include_router(
        crawler.router,
        prefix=f"{settings.API_V1_STR}/crawler",
        tags=["crawler"]
    )
    application.include_router(
        auth.router,
        prefix=f"{settings.API_V1_STR}",
        tags=["auth"]
    )
    application.include_router(
        manual_payment.router,
        prefix=f"{settings.API_V1_STR}/manual",
        tags=["manual_payment"]
    )
    
    @application.get("/")
    async def root():
        return {
            "message": "TradeData Pro API",
            "version": "1.0.0",
            "docs": "/docs",
            "environment": "production" if not settings.DEBUG else "development"
        }
    
    @application.get("/health")
    async def health_check():
        return {"status": "healthy"}
    
    return application

app = create_application()
