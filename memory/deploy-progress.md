# AI 视频生成部署进度

> 开始时间：2026-03-15 14:48
> 硬件：RTX 4050 Laptop 6GB VRAM

---

## 部署计划

### 组件清单
1. ✅ PyTorch (CUDA 12.1) - 安装中
2. ⬜ ComfyUI - 待安装
3. ⬜ ComfyUI 模型下载
4. ⬜ GPT-SoVITS - 待安装
5. ⬜ MoviePy - 待安装
6. ⬜ Replicate API 配置
7. ⬜ 自动化脚本编写

---

## 模型下载清单

### ComfyUI 必备模型（免费）

| 模型 | 大小 | 用途 | 下载地址 |
|------|------|------|----------|
| SDXL Base | 6.9GB | 图像生成 | HuggingFace |
| SDXL Refiner | 6.1GB | 图像优化 | HuggingFace |
| RealVisXL | 6.5GB | 写实风格 | Civitai |
| SD 1.5 | 4.3GB | 低配备选 | HuggingFace |

**合计约：20GB+**

### GPT-SoVITS 模型（免费）
- 预训练模型：约 2GB
- 语音合成底模：约 1GB

---

## 预计时间
- 环境安装：30-60 分钟
- 模型下载：2-4 小时（取决于网速）
- 配置测试：30 分钟
- **总计：3-5 小时**

---

## 费用清单

### 一次性费用
- 模型下载：免费（HuggingFace/Civitai）

### 使用费用（Replicate API）
- Wan 2.1 视频生成：$0.002-0.005/秒
- 预估月费用：¥50-100（100条视频）

---

## 当前状态

- ✅ **SiliconFlow 方案已配置完成**
- ✅ API 调用脚本已编写
- ✅ 配置文档已更新
- ⬜ 等待用户注册并配置 API Key
- ⬜ 等待首次测试运行

## 已完成交付物

1. `workspace/.env` - API Key 配置文件
2. `workspace/scripts/auto_video.py` - 主入口（自动选择 API）
3. `workspace/scripts/siliconflow_video.py` - SiliconFlow 专用脚本
4. `workspace/scripts/batch_generate.py` - 批量生成
5. `workspace/SILICONFLOW_SETUP.md` - 详细配置指南
6. `workspace/README.md` - 快速上手指南

## 费用对比更新

| 平台 | 100条视频/月 | 备注 |
|------|-------------|------|
| Replicate | ¥50-100 | 需国际支付 |
| **SiliconFlow** | **¥30-50** | ✅ 微信/支付宝 |

**SiliconFlow 成本更低，且国内访问稳定！**
