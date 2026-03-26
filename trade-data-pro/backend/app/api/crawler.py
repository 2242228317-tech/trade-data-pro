from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import Optional
from enum import Enum

router = APIRouter()

class CrawlerSource(str, Enum):
    ALIBABA_1688 = "1688"
    CUSTOMS = "customs"
    BOTH = "both"

class CrawlerTaskCreate(BaseModel):
    source: CrawlerSource
    keyword: Optional[str] = None
    category: Optional[str] = None
    max_items: int = 100
    scheduled: bool = False
    schedule_cron: Optional[str] = None  # 例如: "0 2 * * *" 每天2点

class CrawlerTaskResponse(BaseModel):
    task_id: str
    status: str
    message: str

@router.post("/start", response_model=CrawlerTaskResponse)
async def start_crawler(
    task: CrawlerTaskCreate,
    background_tasks: BackgroundTasks
):
    """启动爬虫任务"""
    # TODO: 实现爬虫任务启动逻辑
    
    return {
        "task_id": "task-001",
        "status": "running",
        "message": f"开始爬取 {task.source} 数据，预计处理 {task.max_items} 条"
    }

@router.get("/tasks")
async def get_tasks(
    status: Optional[str] = None,
    page: int = 1,
    page_size: int = 20
):
    """获取爬虫任务列表"""
    return {
        "total": 0,
        "tasks": []
    }

@router.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    """获取任务状态"""
    return {
        "task_id": task_id,
        "status": "running",
        "progress": 45,
        "total_items": 100,
        "success_items": 45,
        "error_items": 0,
        "started_at": "2024-03-16T10:00:00",
        "estimated_complete": "2024-03-16T10:30:00"
    }

@router.post("/tasks/{task_id}/stop")
async def stop_task(task_id: str):
    """停止爬虫任务"""
    return {"message": f"任务 {task_id} 已停止"}

@router.get("/stats")
async def get_crawler_stats():
    """获取爬虫统计信息"""
    return {
        "total_tasks": 0,
        "running_tasks": 0,
        "completed_tasks": 0,
        "failed_tasks": 0,
        "total_data_collected": 0,
        "last_24h_data": 0
    }

@router.post("/schedule")
async def create_scheduled_task(task: CrawlerTaskCreate):
    """创建定时爬虫任务"""
    if not task.scheduled or not task.schedule_cron:
        raise HTTPException(status_code=400, detail="请提供有效的 cron 表达式")
    
    return {
        "schedule_id": "sched-001",
        "cron": task.schedule_cron,
        "message": "定时任务已创建"
    }
