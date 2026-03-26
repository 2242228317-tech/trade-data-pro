"""
批量视频生成脚本
支持从 JSON 文件读取任务列表
"""

import json
import os
from auto_video import create_full_video

CONFIG_FILE = "config.json"

def load_tasks():
    """加载任务列表"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"tasks": []}

def batch_process(max_tasks=None):
    """批量处理任务"""
    config = load_tasks()
    tasks = config.get("tasks", [])
    
    if not tasks:
        print("没有待处理的任务")
        return
    
    print(f"找到 {len(tasks)} 个任务")
    print(f"预计费用: ¥{len(tasks) * 0.5:.1f} - ¥{len(tasks) * 1.5:.1f}")
    print()
    
    confirm = input("确认开始? (y/n): ")
    if confirm.lower() != "y":
        return
    
    completed = 0
    failed = 0
    
    for i, task in enumerate(tasks[:max_tasks] if max_tasks else tasks):
        print(f"\n[{i+1}/{len(tasks)}] {task.get('title', '未命名')}")
        try:
            create_full_video(task)
            completed += 1
        except Exception as e:
            print(f"[失败] {e}")
            failed += 1
    
    print(f"\n批量处理完成: 成功 {completed}, 失败 {failed}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--limit":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        batch_process(max_tasks=limit)
    else:
        batch_process()
