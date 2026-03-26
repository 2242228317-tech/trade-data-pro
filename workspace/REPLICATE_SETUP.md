# Replicate API 配置指南

## 方式一：.env 文件（推荐，最简单）

1. 打开 `workspace/.env` 文件
2. 把 `REPLICATE_API_TOKEN=` 后面的值换成你的 token
3. 保存即可

```
REPLICATE_API_TOKEN=r8_你的token
```

## 方式二：系统环境变量

### Windows PowerShell
```powershell
[Environment]::SetEnvironmentVariable("REPLICATE_API_TOKEN", "你的token", "User")
```

验证：
```powershell
echo $env:REPLICATE_API_TOKEN
```

---

## 注册账号
访问 https://replicate.com/
- 点击 "Sign Up"
- 可用 GitHub/Google 账号直接登录

## 获取 API Token
1. 登录后点击右上角头像
2. 选择 "API tokens"
3. 点击 "Create a new token"
4. 复制 token（格式：r8_xxxxxxxxxxxx）

---
保存为 test_replicate.py：

```python
import os
import replicate

# 测试图像生成
output = replicate.run(
    "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",
    input={"prompt": "a photo of an astronaut riding a horse"}
)
print(output)
```

运行：
```bash
pip install replicate
python test_replicate.py
```

## 5. 视频生成示例
```python
import replicate

# Wan 2.1 文本生成视频
output = replicate.run(
    "wavespeedai/wan-2.1-t2v-720p",
    input={
        "prompt": "A futuristic city at sunset, flying cars, neon lights",
        "num_frames": 81,  # 约 3 秒
        "fps": 24
    }
)
print(output)
```

## 模型价格参考

| 模型 | 价格 | 用途 |
|------|------|------|
| SDXL | $0.01/张 | 图像生成 |
| Wan 2.1 480p | $0.002/秒 | 视频生成 |
| Wan 2.1 720p | $0.005/秒 | 视频生成 |
| ElevenLabs TTS | $0.03/字符 | 语音合成 |

## 免费额度
- 新账号有 $5 免费额度
- 足够测试约 50-100 条短视频
