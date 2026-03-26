# AI 视频生成 - 完整部署手册

## 快速开始（推荐）

由于网络不稳定，建议使用以下分步部署方案：

### 方法一：自动安装（网络稳定时）
1. 双击运行 `install_env.bat`
2. 等待安装完成（约 30-60 分钟）
3. 按提示配置 Replicate API

### 方法二：手动安装（推荐现在使用）

#### 步骤 1：下载 ComfyUI（手动）
访问 https://github.com/comfyanonymous/ComfyUI/releases
下载最新 `ComfyUI_windows_portable_nvidia.7z`
解压到工作目录

#### 步骤 2：安装 Python 依赖
```bash
pip install moviepy pillow numpy replicate
```

#### 步骤 3：配置 Replicate
见 REPLICATE_SETUP.md

---

## 目录结构

```
workspace/
├── ComfyUI/              # 图像生成（手动下载）
├── GPT-SoVITS/           # 语音合成（待安装）
├── scripts/              # 自动化脚本
├── output/               # 输出目录
├── models/               # 模型文件
└── config.json           # 配置文件
```

---

## 模型下载地址

### 必装模型

1. **SDXL Base**（图像生成）
   - 地址：https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0
   - 文件：`sd_xl_base_1.0.safetensors` (6.9GB)
   - 放置：`ComfyUI/models/checkpoints/`

2. **RealVisXL**（写实风格，推荐）
   - 地址：https://civitai.com/models/139562/realvisxl-v40
   - 文件：`RealVisXL_V4.0.safetensors` (6.5GB)
   - 放置：`ComfyUI/models/checkpoints/`

3. **VAE**（图像解码）
   - 地址：https://huggingface.co/madebyollin/sdxl-vae-fp16-fix
   - 文件：`sdxl_vae.safetensors` (300MB)
   - 放置：`ComfyUI/models/vae/`

---

## 费用预算

### 一次性
- 模型下载：免费
- 软件安装：免费

### 每月使用（100条视频）
- Replicate API：约 ¥50-100
- 电费：约 ¥20

---

## 开始使用

环境准备好后，运行：
```bash
python scripts/auto_video.py --prompt "你的视频描述"
```
