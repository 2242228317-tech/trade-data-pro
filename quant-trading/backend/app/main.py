from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .models import init_db
from .routers import stock, indicators, strategy, backtest

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时初始化
    init_db()
    yield
    # 关闭时清理

app = FastAPI(
    title="量化交易系统 API",
    description="基于Python的量化交易平台，提供股票数据、技术指标、策略交易和回测功能",
    version="1.0.0",
    lifespan=lifespan
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制为前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(stock.router)
app.include_router(indicators.router)
app.include_router(strategy.router)
app.include_router(backtest.router)

@app.get("/")
def root():
    return {
        "message": "量化交易系统 API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "stocks": "/api/stocks",
            "indicators": "/api/indicators",
            "strategy": "/api/strategy",
            "backtest": "/api/backtest"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": __import__('datetime').datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
