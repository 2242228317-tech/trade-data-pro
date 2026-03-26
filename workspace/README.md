# 🤖 AI 视频生成工作站（SiliconFlow 版）

已配置完成！支持 **SiliconFlow API**，国内直接访问，微信/支付宝支付。

---

## 🚀 快速开始（3步）

### 第 1 步：注册 SiliconFlow
1. 访问 https://siliconflow.cn/
2. 点击右上角"注册"，用手机号注册
3. 完成实名认证（如需要）

### 第 2 步：获取 API Key
1. 登录后，点击右上角头像 → "API 密钥"
2. 点击 "新建 API 密钥"
3. 复制密钥（格式：`sk-xxxxxxxx`）
4. 粘贴到 `workspace/.env` 文件：
```
SILICONFLOW_API_KEY=sk-你的key
```

### 第 3 步：充值（可选）
- 新用户有免费额度
- 如需充值：头像 → "账户余额" → "充值"
- 建议先充 **¥10** 测试

### 第 4 步：运行测试
```bash
cd C:\Users\22422\.openclaw\workspace\workspace
python scripts\auto_video.py
```

---

## 💰 费用说明

| 模型 | 价格 | 5秒视频成本 |
|------|------|-------------|
| Wan2.1-T2V-14B | ¥0.08/秒 | ¥0.4 |
| HunyuanVideo | ¥0.06/秒 | ¥0.3 |

**100条视频/月：约 ¥30-50**

---

## 📝 使用示例

### 生成单个视频
```python
from scripts.siliconflow_video import generate_video

video_path = generate_video(
    prompt="一只熊猫在竹林里吃竹子，阳光明媚",
    model="Wan-AI/Wan2.1-T2V-14B",
    seconds=5
)
```

### 批量生成
编辑 `config.json`，添加任务列表后运行：
```bash
python scripts\batch_generate.py
```

---

## 🎬 支持的视频模型

| 模型 | 特点 | 推荐场景 |
|------|------|----------|
| **Wan2.1-T2V-14B** | 画质最好，720P | 高质量短视频 |
| **HunyuanVideo** | 速度快，性价比高 | 批量生产 |

---

## 📁 文件结构

```
workspace/
├── .env                    # API Key 配置
├── scripts/
│   ├── auto_video.py       # 主入口（自动选择 API）
│   ├── siliconflow_video.py # SiliconFlow 专用
│   └── batch_generate.py   # 批量生成
├── output/                 # 输出目录
├── SILICONFLOW_SETUP.md    # 详细配置指南
└── README.md               # 本文件
```

---

## ⚡ 性能参考

| 视频时长 | 生成时间 | 费用 |
|----------|----------|------|
| 5秒 | 约 1-2 分钟 | ¥0.3-0.4 |
| 10秒 | 约 2-4 分钟 | ¥0.6-0.8 |

---

**现在就去注册 SiliconFlow 开始生成视频吧！**

遇到问题随时问我。
