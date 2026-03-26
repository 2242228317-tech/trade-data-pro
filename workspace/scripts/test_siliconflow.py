"""
SiliconFlow 图像生成测试
使用免费模型验证 API 连接
"""

import os
import sys
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

API_KEY = os.environ.get("SILICONFLOW_API_KEY")
BASE_URL = "https://api.siliconflow.cn/v1"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

if not API_KEY:
    print("[错误] 未找到 SILICONFLOW_API_KEY")
    sys.exit(1)

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def generate_image(prompt, model="Qwen/Qwen-Image"):
    """
    测试图像生成
    免费模型: stabilityai/stable-diffusion-3-medium
    """
    print(f"[图像生成测试]")
    print(f"模型: {model}")
    print(f"提示词: {prompt}")
    
    url = f"{BASE_URL}/images/generations"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "size": "1024x1024",
        "n": 1
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        image_url = result["data"][0]["url"]
        
        # 下载图像
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_image_{timestamp}.png"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        img_response = requests.get(image_url)
        with open(filepath, 'wb') as f:
            f.write(img_response.content)
        
        print(f"[成功] 图像保存至: {filepath}")
        return filepath
    else:
        print(f"[失败] {response.text}")
        return None

def check_account():
    """检查账户信息"""
    print("\n[检查账户信息]")
    
    url = f"{BASE_URL}/user/info"
    response = requests.get(url, headers=headers, timeout=30)
    
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        info = response.json()
        print(f"账户信息: {info}")
    else:
        print(f"查询失败: {response.text}")

def check_balance():
    """检查账户余额"""
    print("\n[检查账户余额]")
    
    url = f"{BASE_URL}/user/balance"
    response = requests.get(url, headers=headers, timeout=30)
    
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        balance = response.json()
        print(f"余额信息: {balance}")
    else:
        print(f"查询失败: {response.text}")
    """检查可用的模型列表"""
    print("\n[检查可用模型]")
    
    url = f"{BASE_URL}/models"
    response = requests.get(url, headers=headers, timeout=30)
    
    if response.status_code == 200:
        models = response.json()
        print(f"找到 {len(models.get('data', []))} 个模型")
        
        # 过滤视频和图像模型
        video_models = [m for m in models.get('data', []) if 'video' in m.get('id', '').lower()]
        image_models = [m for m in models.get('data', []) if any(x in m.get('id', '').lower() for x in ['image', 'sd', 'diffusion'])]
        
        print(f"\n视频模型: {len(video_models)}")
        for m in video_models[:5]:
            print(f"  - {m.get('id')}")
            
        print(f"\n图像模型: {len(image_models)}")
        for m in image_models[:5]:
            print(f"  - {m.get('id')}")
    else:
        print(f"查询失败: {response.status_code}")

if __name__ == "__main__":
    print("="*50)
    print("SiliconFlow API 测试")
    print("="*50)
    print()
    
    # 先检查账户
    check_account()
    check_balance()
    
    print("\n" + "="*50)
    print("测试图像生成...")
    print("="*50)
    
    # 测试图像生成
    result = generate_image("a cute panda eating bamboo, watercolor style")
