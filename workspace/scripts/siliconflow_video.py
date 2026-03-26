"""
SiliconFlow API 视频生成脚本
支持：Wan2.1-T2V、HunyuanVideo
"""

import os
import sys
import time
import requests
from datetime import datetime

# 加载环境变量
def load_env():
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

load_env()

# 配置
API_KEY = os.environ.get("SILICONFLOW_API_KEY")
BASE_URL = "https://api.siliconflow.cn/v1"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

if not API_KEY:
    print("[错误] 未找到 SILICONFLOW_API_KEY")
    print("请在 .env 文件中设置你的 API Key")
    sys.exit(1)

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def submit_video_job(prompt, model="Tencent/HunyuanVideo", seconds=5):
    """
    提交视频生成任务
    
    模型选项：
    - Tencent/HunyuanVideo (混元视频，推荐)
    - Wan-AI/Wan2.1-T2V-14B (文生视频)
    """
    print(f"[提交任务] 模型: {model}")
    print(f"[提示词] {prompt[:60]}...")
    
    url = f"{BASE_URL}/video/submit"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "duration": seconds,  # 秒数
        "resolution": "720p"  # 480p, 720p
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        request_id = result.get("requestId")
        print(f"[成功] 任务ID: {request_id}")
        return request_id
    else:
        print(f"[错误] {response.status_code}: {response.text}")
        return None

def query_video_status(request_id):
    """查询任务状态"""
    url = f"{BASE_URL}/video/status"
    
    payload = {"requestId": request_id}
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"[查询错误] {response.status_code}: {response.text}")
        return None

def download_video(url, filename):
    """下载视频"""
    print(f"[下载中] 视频文件...")
    response = requests.get(url, stream=True, timeout=120)
    
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    
    print(f"[完成] 保存至: {filepath}")
    return filepath

def generate_video(prompt, model="Tencent/HunyuanVideo", seconds=5, max_wait=300):
    """
    完整的视频生成流程
    
    Args:
        prompt: 视频描述
        model: 模型名称
        seconds: 视频时长（秒）
        max_wait: 最大等待时间（秒）
    
    Returns:
        视频文件路径
    """
    # 提交任务
    request_id = submit_video_job(prompt, model, seconds)
    if not request_id:
        return None
    
    # 轮询等待
    print(f"[等待生成] 预计 {seconds * 10}-{seconds * 20} 秒...")
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        time.sleep(5)
        status = query_video_status(request_id)
        
        if not status:
            continue
        
        state = status.get("status")
        print(f"[状态] {state}", end="\r")
        
        if state == "SUCCEEDED":
            print(f"\n[成功] 视频生成完成！")
            video_url = status.get("videoUrl")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"siliconflow_video_{timestamp}.mp4"
            return download_video(video_url, filename)
        
        elif state in ["FAILED", "CANCELLED"]:
            print(f"\n[失败] 任务状态: {state}")
            return None
    
    print(f"\n[超时] 超过最大等待时间")
    return None

if __name__ == "__main__":
    print("="*50)
    print("SiliconFlow 视频生成测试")
    print("="*50)
    print()
    
    # 测试生成
    test_prompt = "一只可爱的熊猫在竹林里吃竹子，阳光明媚，高清画质"
    
    print(f"测试提示: {test_prompt}")
    print()
    
    # 先尝试 HunyuanVideo
    result = generate_video(test_prompt, model="Tencent/HunyuanVideo", seconds=5)
    
    if not result:
        print("\n尝试其他模型...")
        result = generate_video(test_prompt, model="Wan-AI/Wan2.1-T2V-14B", seconds=5)
    
    if result:
        print(f"\n✅ 视频生成成功: {result}")
    else:
        print(f"\n❌ 视频生成失败")
