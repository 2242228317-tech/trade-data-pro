@echo off
echo ====================================
echo  TradeData Pro - 手动支付版
echo ====================================
echo.
echo 正在启动服务...
echo.

echo [1/2] 启动后端服务...
start "后端: http://localhost:8000" cmd /k "cd backend && uvicorn app.main:app --port 8000"

echo [2/2] 启动前端服务...
timeout /t 3 /nobreak > nul
start "前端: http://localhost:3001" cmd /k "cd frontend && npm run dev"

echo.
echo ====================================
echo  服务启动成功！
echo ====================================
echo.
echo 访问地址:
echo   - 网站首页: http://localhost:3001
echo   - 定价页面: http://localhost:3001/pricing
echo   - 管理后台: http://localhost:3001/admin
echo.
echo 管理密码: trade888
echo.
echo 按任意键关闭所有服务...
pause > nul

taskkill /FI "WINDOWTITLE eq 后端: http://localhost:8000*" /F > nul 2>&1
taskkill /FI "WINDOWTITLE eq 前端: http://localhost:3001*" /F > nul 2>&1

echo 服务已关闭
timeout /t 2 > nul
