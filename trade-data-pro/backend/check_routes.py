import requests

# 获取 OpenAPI 文档
response = requests.get('http://localhost:8000/openapi.json')
data = response.json()

print("可用路由:")
for path, methods in data.get('paths', {}).items():
    for method, info in methods.items():
        if method in ['get', 'post', 'put', 'delete']:
            print(f"  {method.upper():6} {path}")
