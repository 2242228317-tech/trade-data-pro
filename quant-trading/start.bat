@echo off
chcp 65001 >nul
echo ==========================================
echo      量化交易系统启动脚本
echo ==========================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.9+
    pause
    exit /b 1
)

REM 检查Node
node --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Node.js，请先安装Node.js 18+
    pause
    exit /b 1
)

echo [1/4] 检查环境... OK
echo.

REM 安装后端依赖
echo [2/4] 安装后端依赖...
cd backend
if not exist ".venv" (
    python -m venv .venv
)
call .venv\Scripts\activate.bat
pip install -r requirements.txt -q
if errorlevel 1 (
    echo [错误] 后端依赖安装失败
    pause
    exit /b 1
)
echo [2/4] 后端依赖安装完成
echo.

REM 启动后端
echo [3/4] 启动后端服务...
start "后端服务" cmd /k "call .venv\Scripts\activate.bat && python -m app.main"
cd ..
timeout /t 3 /nobreak >nul
echo [3/4] 后端服务已启动 (http://localhost:8000)
echo.

REM 安装前端依赖
echo [4/4] 安装前端依赖...
cd frontend
if not exist "node_modules" (
    npm install
    if errorlevel 1 (
        echo [错误] 前端依赖安装失败
        pause
        exit /b 1
    )
)

REM 启动前端
echo [4/4] 启动前端服务...
start "前端服务" cmd /k "npm run dev"
cd ..
timeout /t 3 /nobreak >nul
echo [4/4] 前端服务已启动 (http://localhost:3000)
echo.

echo ==========================================
echo      启动完成！
echo ==========================================
echo.
echo 后端API: http://localhost:8000
echo 前端页面: http://localhost:3000
echo API文档: http://localhost:8000/docs
echo.
echo 按任意键关闭所有服务...
pause >nul

REM 关闭服务
taskkill /FI "WINDOWTITLE eq 后端服务*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq 前端服务*" /F >nul 2>&1
echo 服务已关闭
