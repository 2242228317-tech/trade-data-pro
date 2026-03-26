"""
LiblibAI API 测试脚本
"""

import os
import sys
import requests

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

API_KEY = os.environ.get("LIBLIBAI_API_KEY")
if not API_KEY:
    print("[错误] 未找到 LIBLIBAI_API_KEY")
    sys.exit(1)

print("="*50)
print("LiblibAI API 测试")
print("="*50)
print(f"API Key: {API_KEY[:10]}...{API_KEY[-5:]}")
print()

# 尝试不同的 API 端点
endpoints = [
    "https://liblib-api.vibrou.com/api/generate/image",
    "https://api.liblib.art/api/generate/image",
    "https://www.liblib.art/api/generate/image",
]

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "prompt": "a cute panda eating bamboo",
    "width": 512,
    "height": 512,
    "steps": 20
}

for url in endpoints:
    print(f"[测试] {url}")
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        print(f"状态: {response.status_code}")
        if response.status_code == 200:
            print(f"成功! 响应: {response.text[:200]}")
            break
        else:
            print(f"响应: {response.text[:100]}")
    except Exception as e:
        print(f"错误: {e}")
    print()
