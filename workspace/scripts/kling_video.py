"""
可灵AI (KlingAI) 视频生成脚本
支持文生视频
API文档: https://app.klingai.com/cn/dev/document-api
"""

import os
import time
import jwt
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

# API配置
BASE_URL = "https://api-beijing.klingai.com"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_credentials():
    """获取API凭证，支持运行时重新加载"""
    access_key = os.environ.get("KLING_ACCESS_KEY")
    secret_key = os.environ.get("KLING_SECRET_KEY")
    
    # 如果环境变量不存在，尝试从 .env 文件重新加载
    if not access_key or not secret_key:
        load_env()
        access_key = os.environ.get("KLING_ACCESS_KEY")
        secret_key = os.environ.get("KLING_SECRET_KEY")
    
    return access_key, secret_key

def generate_jwt_token():
    """生成JWT Token"""
    access_key, secret_key = get_credentials()
    
    if not access_key or not secret_key:
        raise ValueError("KLING_ACCESS_KEY or KLING_SECRET_KEY not found")
    
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    payload = {
        "iss": access_key,
        "exp": int(time.time()) + 3600,  # 1小时过期
        "nbf": int(time.time()) - 5
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256", headers=headers)
    return token

def get_auth_headers():
    """获取带鉴权的请求头"""
    try:
        token = generate_jwt_token()
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
    except ValueError as e:
        print(f"[Error] {e}")
        return None

def submit_text_to_video(prompt, model="kling-v1-6", duration=5, aspect_ratio="16:9"):
    """
    提交文生视频任务
    
    Args:
        prompt: 视频描述
        model: 模型版本 (kling-v1-6, kling-v1-5, etc.)
        duration: 时长(秒)
        aspect_ratio: 比例 (16:9, 9:16, 1:1)
    """
    url = f"{BASE_URL}/v1/videos/text2video"
    
    headers = get_auth_headers()
    if not headers:
        return None
    
    payload = {
        "model": model,
        "prompt": prompt,
        "negative_prompt": "",
        "cfg_scale": 0.5,
        "duration": duration,
        "aspect_ratio": aspect_ratio
    }
    
    print(f"[Submit] {prompt[:50]}...")
    print(f"[Model] {model}")
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        print(f"[Status] {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
            except ValueError as e:
                print(f"[Error] Invalid JSON response: {e}")
                return None
            
            if result.get("code") == 0:
                task_id = result["data"]["task_id"]
                print(f"[Success] Task ID: {task_id}")
                return task_id
            else:
                print(f"[Error] {result.get('message')}")
                return None
        else:
            print(f"[Error] HTTP {response.status_code}: {response.text[:200]}")
            return None
    except Exception as e:
        print(f"[Exception] {e}")
        return None

def query_video_result(task_id):
    """查询视频生成结果"""
    url = f"{BASE_URL}/v1/videos/{task_id}"
    headers = get_auth_headers()
    if not headers:
        return None
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            try:
                result = response.json()
            except ValueError as e:
                print(f"[Error] Invalid JSON response: {e}")
                return None
            
            if result.get("code") == 0:
                data = result["data"]
                status = data.get("status")
                
                status_map = {
                    "submitted": "Submitted",
                    "processing": "Processing",
                    "succeed": "Success",
                    "failed": "Failed"
                }
                print(f"[Status] {status_map.get(status, status)}")
                
                if status == "succeed":
                    video_url = data.get("video_url")
                    return video_url
                elif status == "failed":
                    print(f"[Failed] {data.get('message', 'Unknown')}")
                    return None
                else:
                    return None
        return None
    except Exception as e:
        print(f"[Exception] {e}")
        return None

def download_video(video_url, filename=None):
    """下载视频"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"kling_video_{timestamp}.mp4"
    
    filepath = os.path.join(OUTPUT_DIR, filename)
    
    print(f"[Downloading] ...")
    try:
        response = requests.get(video_url, stream=True, timeout=120)
        
        if response.status_code != 200:
            print(f"[Download Failed] HTTP {response.status_code}")
            return None
        
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        # 验证文件大小
        file_size = os.path.getsize(filepath)
        if file_size == 0:
            print(f"[Download Failed] Empty file")
            os.remove(filepath)
            return None
        
        print(f"[Saved] {filepath} ({file_size/1024/1024:.2f} MB)")
        return filepath
    except Exception as e:
        print(f"[Download Failed] {e}")
        return None

def estimate_wait_time(duration):
    """
    根据视频时长估算等待时间
    可灵生成时间：短视频快，长视频慢，且受服务器负载影响
    """
    if duration <= 5:
        return (30, 90)      # 5秒视频：30-90秒
    elif duration <= 10:
        return (60, 180)     # 10秒视频：1-3分钟
    else:
        return (120, 300)    # 更长视频：2-5分钟

def generate_video(prompt, model="kling-v1-6", duration=5, max_wait=None):
    """
    完整的视频生成流程
    
    Args:
        prompt: 视频描述
        model: 模型版本
        duration: 视频时长(秒)
        max_wait: 最大等待时间(秒)，默认根据时长自动计算
    
    Returns:
        视频文件路径
    """
    # 提交任务
    task_id = submit_text_to_video(prompt, model, duration)
    if not task_id:
        return None
    
    # 根据时长计算预估时间和超时
    est_min, est_max = estimate_wait_time(duration)
    if max_wait is None:
        max_wait = est_max * 2  # 超时设为预估最大值的2倍
    
    print(f"[Waiting] Estimated {est_min}-{est_max}s (timeout: {max_wait}s)")
    start_time = time.time()
    check_interval = 10  # 前30秒每10秒查一次
    
    while time.time() - start_time < max_wait:
        elapsed = time.time() - start_time
        
        # 超过预估时间后，降低查询频率
        if elapsed > est_max and check_interval < 30:
            check_interval = 30
            print(f"[Slow] Exceeded estimate, checking every {check_interval}s...")
        
        time.sleep(check_interval)
        video_url = query_video_result(task_id)
        
        if video_url:
            actual_time = int(time.time() - start_time)
            print(f"[Done] Generated in {actual_time}s")
            return download_video(video_url)
    
    print(f"[Timeout] Waited {int(time.time() - start_time)}s, max: {max_wait}s")
    return None

if __name__ == "__main__":
    print("="*50)
    print("KlingAI Video Generation")
    print("="*50)
    print()
    
    test_prompt = "A cute panda eating bamboo in sunlight, high quality"
    
    print(f"Prompt: {test_prompt}")
    print()
    
    result = generate_video(test_prompt, duration=5)
    
    if result:
        print(f"\n[SUCCESS] Video: {result}")
    else:
        print(f"\n[FAILED]")
