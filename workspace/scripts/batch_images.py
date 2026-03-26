"""
SiliconFlow 图像批量生成
使用 Qwen 图像模型
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

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def generate_image(prompt, model="Qwen/Qwen-Image", size="1024x1024"):
    """生成单张图像"""
    print(f"[生成] {prompt[:50]}...")
    
    url = f"{BASE_URL}/images/generations"
    
    payload = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "n": 1
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    
    if response.status_code == 200:
        result = response.json()
        image_url = result["data"][0]["url"]
        
        # 下载
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"img_{timestamp}.png"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        img_response = requests.get(image_url)
        with open(filepath, 'wb') as f:
            f.write(img_response.content)
        
        print(f"[完成] {filepath}")
        return filepath
    else:
        print(f"[失败] {response.status_code}: {response.text[:100]}")
        return None

def batch_generate(prompts):
    """批量生成"""
    print("="*50)
    print(f"批量生成 {len(prompts)} 张图像")
    print("="*50)
    
    results = []
    for i, prompt in enumerate(prompts):
        print(f"\n[{i+1}/{len(prompts)}]")
        result = generate_image(prompt)
        if result:
            results.append(result)
    
    print(f"\n完成: 成功 {len(results)}/{len(prompts)}")
    return results

if __name__ == "__main__":
    # 测试批量生成
    test_prompts = [
        "a cute panda eating bamboo, watercolor style",
        "futuristic cyberpunk city at night, neon lights",
        "serene mountain landscape, sunrise, misty"
    ]
    
    batch_generate(test_prompts)
