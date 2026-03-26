"""
LiblibAI 视频生成脚本
支持可灵(Kling)文生视频
"""

import os
import sys
import time
import hmac
import hashlib
import base64
import requests
from datetime import datetime
from urllib.parse import urlparse

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

# API 配置
ACCESS_KEY = os.environ.get("LIBLIBAI_ACCESS_KEY", "qgyGt2MUHRae6hhbZ_tZvA")
SECRET_KEY = os.environ.get("LIBLIBAI_SECRET_KEY", "IlYsGsFS7tVkPGlCG2PsbQ8xHeqbaokt")
BASE_URL = "https://api.liblib.art"  # 尝试 API 子域名
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

if not ACCESS_KEY or not SECRET_KEY:
    print("[错误] 未找到 LiblibAI API Key")
    sys.exit(1)

def generate_sign(path, timestamp):
    """生成签名"""
    # 签名格式: Base64(HMAC-SHA256(SECRET_KEY, PATH + TIMESTAMP))
    message = f"{path}{timestamp}"
    signature = hmac.new(
        SECRET_KEY.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).digest()
    return base64.b64encode(signature).decode('utf-8')

def get_headers(path):
    """获取请求头"""
    timestamp = str(int(time.time()))
    sign = generate_sign(path, timestamp)
    
    return {
        "Content-Type": "application/json",
        "AccessKey": ACCESS_KEY,
        "Signature": sign,
        "Timestamp": timestamp
    }

def submit_video_task(prompt, model="kling-v2-1-master", duration=5, aspect_ratio="16:9"):
    """
    提交文生视频任务
    """
    # 尝试不同的路径
    paths = [
        "/api/generate/video/kling/text2video",
        "/api/v1/generate/video/kling/text2video",
    ]
    
    for path in paths:
        url = f"{BASE_URL}{path}"
        headers = get_headers(path)
        
        payload = {
            "templateUuid": "61cd8b60d340404394f2a545eeaf197a",
            "generateParams": {
                "model": model,
                "prompt": prompt,
                "promptMagic": 1,
                "aspectRatio": aspect_ratio,
                "duration": str(duration),
                "sound": "on",
                "mode": "std"
            }
        }
        
        print(f"[尝试] {path}")
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            print(f"[状态] {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get("code") == 0:
                    task_uuid = result["data"]["generateUuid"]
                    print(f"[成功] 任务ID: {task_uuid}")
                    return task_uuid
                else:
                    print(f"[错误] {result.get('msg')}")
                    return None
        except Exception as e:
            print(f"[异常] {e}")
            continue
    
    print("[失败] 所有路径都失败了")
    return None

def query_video_result(task_uuid):
    """查询视频生成结果"""
    path = "/api/generate/video/kling/result"
    url = f"{BASE_URL}{path}"
    
    headers = get_headers(path)
    payload = {"generateUuid": task_uuid}
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if result.get("code") == 0:
                data = result["data"]
                status = data.get("generateStatus")
                
                # 状态说明: 0-排队中 1-生成中 2-成功 3-失败
                status_map = {0: "排队中", 1: "生成中", 2: "成功", 3: "失败"}
                print(f"[状态] {status_map.get(status, status)}")
                
                if status == 2:  # 成功
                    video_url = data.get("videoUrl")
                    return video_url
                elif status == 3:  # 失败
                    print(f"[失败原因] {data.get('generateMsg', '未知')}")
                    return None
                else:
                    return None
        return None
    except Exception as e:
        print(f"[异常] {e}")
        return None

def download_video(video_url, filename=None):
    """下载视频"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"liblib_video_{timestamp}.mp4"
    
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    print(f"[下载中] ...")
    try:
        response = requests.get(video_url, stream=True, timeout=120)
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"[完成] 保存至: {filepath}")
        return filepath
    except Exception as e:
        print(f"[下载失败] {e}")
        return None

def generate_video(prompt, model="kling-v2-1-master", duration=5, max_wait=300):
    """
    完整的视频生成流程
    
    Returns:
        视频文件路径
    """
    # 提交任务
    task_uuid = submit_video_task(prompt, model, duration)
    if not task_uuid:
        return None
    
    # 轮询等待结果
    print(f"[等待生成] 预计 {duration * 20}-{duration * 40} 秒...")
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        time.sleep(10)
        video_url = query_video_result(task_uuid)
        
        if video_url:
            return download_video(video_url)
        
        # 如果失败，会返回 None 且状态已打印
    
    print("[超时] 超过最大等待时间")
    return None

if __name__ == "__main__":
    print("="*50)
    print("LiblibAI Video Generation Test")
    print("="*50)
    print()
    
    test_prompt = "a cute panda eating bamboo in sunlight, high quality"
    
    print(f"Prompt: {test_prompt}")
    print()
    
    result = generate_video(test_prompt, duration=5)
    
    if result:
        print(f"\n[SUCCESS] Video saved: {result}")
    else:
        print(f"\n[FAILED] Video generation failed")
