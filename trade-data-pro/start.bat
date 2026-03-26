@echo off
chcp 65001 >nul
echo ==========================================
echo    TradeData Pro 启动脚本
echo ==========================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

REM 检查Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Node.js，请先安装 Node.js 18+
    pause
    exit /b 1
)

echo [1/4] 安装后端依赖...
cd backend
pip install -q -r requirements.txt
if errorlevel 1 (
    echo [错误] 后端依赖安装失败
    pause
    exit /b 1
)

echo [2/4] 初始化数据库...
python -c "from app.models.database import init_db; init_db(); print('数据库初始化完成')"

echo [3/4] 安装前端依赖...
cd ..\frontend
call npm install >nul 2>&1
if errorlevel 1 (
    echo [错误] 前端依赖安装失败
    pause
    exit /b 1
)

echo [4/4] 构建前端...
call npm run build >nul 2>&1
if errorlevel 1 (
    echo [警告] 前端构建失败，将使用开发模式
)

cd ..
echo.
echo ==========================================
echo    启动服务...
echo ==========================================
echo.
echo 访问地址：
echo   - 前端: http://localhost:3000
echo   - 后端: http://localhost:8000
echo   - API文档: http://localhost:8000/docs
echo.
echo 按 Ctrl+C 停止服务
echo.

REM 使用 start 命令在新窗口启动后端
start "TradeData Pro Backend" cmd /k "cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"

REM 等待后端启动
timeout /t 3 /nobreak >nul

REM 在新窗口启动前端
start "TradeData Pro Frontend" cmd /k "cd frontend && npm run dev"

echo 服务已启动！
pause
