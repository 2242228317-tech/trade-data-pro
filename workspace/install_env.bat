@echo off
chcp 65001 >nul
echo ==========================================
echo   AI 视频生成环境一键安装脚本
echo ==========================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.10+
    pause
    exit /b 1
)

echo [1/6] 创建虚拟环境...
python -m venv venv
call venv\Scripts\activate.bat

echo [2/6] 升级 pip...
python -m pip install --upgrade pip -q

echo [3/6] 安装 PyTorch (CUDA 12.1)...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

echo [4/6] 安装 MoviePy 和依赖...
pip install moviepy pillow numpy scipy

echo [5/6] 安装 Replicate API...
pip install replicate

echo [6/6] 安装其他工具...
pip install requests tqdm

echo.
echo ==========================================
echo   基础环境安装完成！
echo ==========================================
echo.
echo 下一步：
echo 1. 下载 ComfyUI: git clone https://github.com/comfyanonymous/ComfyUI.git
echo 2. 配置 Replicate API Token
echo 3. 运行测试脚本
echo.
pause
