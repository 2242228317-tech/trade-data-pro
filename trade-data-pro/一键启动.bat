@echo off
chcp 65001 >nul
echo ====================================
echo   TradeData Pro - 启动脚本
echo ====================================
echo.
echo 本机IP: 172.20.10.2
echo.
echo 访问地址:
echo   - 本机: http://localhost:3000
echo   - 局域网: http://172.20.10.2:3000
echo.

echo [1/2] 启动后端服务...
start "后端: http://172.20.10.2:8000" cmd /k "cd /d %~dp0backend && uvicorn app.main:app --port 8000 --host 0.0.0.0"

echo [2/2] 启动前端服务...
timeout /t 3 /nobreak > nul
start "前端: http://172.20.10.2:3000" cmd /k "cd /d %~dp0frontend && npm run dev -- --hostname 0.0.0.0"

echo.
echo ====================================
echo  服务启动成功！
echo ====================================
echo.
echo 访问地址:
echo   - 本机:     http://localhost:3000
echo   - 局域网:   http://172.20.10.2:3000
echo   - 手机/其他电脑: http://172.20.10.2:3000
echo.
echo 管理后台: http://localhost:3000/admin
echo 密码: trade888
echo.
pause
