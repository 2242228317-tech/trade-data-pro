# 一键配置脚本 - 手动支付方式
# 运行方式: 在 trade-data-pro 目录下执行: python setup_payment.py

import os
import shutil

print("=== TradeData Pro 手动支付配置 ===")
print()

# 1. 创建图片目录
images_dir = os.path.join("frontend", "public", "images")
os.makedirs(images_dir, exist_ok=True)
print("[OK] 创建目录: " + images_dir)

# 2. 检查收款码图片
alipay_path = os.path.join(images_dir, "alipay-qr.png")
wechat_path = os.path.join(images_dir, "wechat-qr.png")

alipay_exists = os.path.exists(alipay_path)
wechat_exists = os.path.exists(wechat_path)

print()
print("收款码检查:")
print("  支付宝: " + ("已存在" if alipay_exists else "需要放入"))
print("  微信: " + ("已存在" if wechat_exists else "需要放入"))

if not alipay_exists or not wechat_exists:
    print()
    print("[!] 请把收款码图片放入: " + os.path.abspath(images_dir))
    print("   - 支付宝收款码 --> 重命名为: alipay-qr.png")
    print("   - 微信收款码 --> 重命名为: wechat-qr.png")
    print()
    print("放好后重新运行这个脚本")
    input("按回车键退出...")
    exit(1)

# 3. 获取账号信息
print()
print("=== 配置账号信息 ===")
alipay_name = input("你的支付宝显示名是什么？(比如:张三) ").strip() or "管理员"
wechat_name = input("你的微信显示名是什么？(比如:李四) ").strip() or "管理员"
admin_key = input("设置管理后台密码: ").strip() or "admin123"

# 4. 修改后端配置
config_file = os.path.join("backend", "app", "api", "manual_payment.py")
with open(config_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 替换配置
content = content.replace(
    '"account": "你的支付宝账号"',
    '"account": "' + alipay_name + '"'
)
content = content.replace(
    '"account": "你的微信账号"',
    '"account": "' + wechat_name + '"'
)
content = content.replace(
    'ADMIN_KEY = "admin123"',
    'ADMIN_KEY = "' + admin_key + '"'
)

with open(config_file, 'w', encoding='utf-8') as f:
    f.write(content)

print()
print("[OK] 配置已更新")

# 5. 生成启动脚本
start_script = '''@echo off
echo 启动 TradeData Pro...
echo.

start "后端服务" cmd /k "cd backend && uvicorn app.main:app --port 8000"
timeout /t 3 /nobreak > nul
start "前端服务" cmd /k "cd frontend && npm run dev"

echo.
echo 服务启动中...
echo 管理后台: http://localhost:3001/admin
echo 密码: ''' + admin_key + '''
echo.
pause
'''

with open("start.bat", "w") as f:
    f.write(start_script)

print("[OK] 生成启动脚本: start.bat")

print()
print("=== 配置完成！===")
print()
print("下次启动只需双击运行: start.bat")
print("管理后台密码: " + admin_key)
print()
print("现在可以测试收款了！")

input("按回车键退出...")
