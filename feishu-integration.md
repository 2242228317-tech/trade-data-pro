# 飞书接入指南 - 律师工具箱

将律师助手接入飞书，让团队在飞书里直接使用法律工具！

---

## 🎯 方案对比

| 方案 | 难度 | 功能 | 推荐场景 |
|------|------|------|----------|
| 飞书机器人 Webhook | ⭐ 简单 | 发送消息 | 通知提醒 |
| 飞书自建应用 | ⭐⭐⭐ 中等 | 完整交互 | 正式使用 |
| 飞书服务台 | ⭐⭐ 简单 | 问答机器人 | 客服场景 |

---

## 📦 方案一：飞书机器人（Webhook）- 5 分钟搞定

### 第 1 步：创建飞书机器人

1. 打开飞书，进入要添加机器人的**群聊**
2. 点击右上角 **「...」** → **「添加机器人」**
3. 点击 **「自定义机器人」** → **「添加」**
4. 设置机器人名称：`律师助手`
5. 选择一个头像（可选）
6. **复制 Webhook 地址**（重要！）

   Webhook 格式：`https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

### 第 2 步：测试机器人

用 curl 测试一下：

```bash
curl -X POST "https://open.feishu.cn/open-apis/bot/v2/hook/你的 webhook 地址" \
  -H "Content-Type: application/json" \
  -d '{
    "msg_type": "text",
    "content": {
      "text": "你好，我是律师助手！⚖️"
    }
  }'
```

### 第 3 步：发送富文本消息

```bash
curl -X POST "https://open.feishu.cn/open-apis/bot/v2/hook/你的 webhook 地址" \
  -H "Content-Type: application/json" \
  -d '{
    "msg_type": "interactive",
    "card": {
      "header": {
        "title": {
          "tag": "plain_text",
          "content": "⚖️ 律师工具箱"
        },
        "template": "blue"
      },
      "elements": [
        {
          "tag": "markdown",
          "content": "**可用工具：**\n- 💰 诉讼费计算器\n- 📈 利息计算器\n- 📄 法律文书生成\n- 📁 案件管理"
        },
        {
          "tag": "action",
          "actions": [
            {
              "tag": "button",
              "text": {
                "tag": "plain_text",
                "content": "打开工具箱"
              },
              "url": "file:///C:/Users/22422/.openclaw/workspace/lawyer-tools/index.html",
              "type": "default"
            }
          ]
        }
      ]
    }
  }'
```

---

## 🔧 方案二：飞书自建应用 - 完整功能

### 第 1 步：创建应用

1. 访问 **[飞书开放平台](https://open.feishu.cn/)**
2. 登录飞书账号
3. 点击 **「创建应用」** → 选择 **「自建应用」**
4. 填写信息：
   - 应用名称：`律师助手`
   - 应用图标：上传一个法律相关的图标
   - 应用描述：`为法律专业人士打造的智能工具集`
5. 点击 **「创建」**

### 第 2 步：记录凭证

创建后，在 **「应用凭证」** 页面记录：
- **App ID**：`cli_xxxxxxxxxxxx`
- **App Secret**：`xxxxxxxxxxxxxxxx`

⚠️ 妥善保管，不要泄露！

### 第 3 步：配置权限

进入 **「权限管理」** 页面，添加以下权限：

```
用户身份权限：
- 以应用身份发送消息
- 读取用户信息

机器人权限：
- 在群聊中发送和接收消息
- 获取群成员列表

可选权限：
- 上传下载文件
- 创建和管理云文档
```

点击 **「申请权限」** 并提交。

### 第 4 步：配置事件订阅

1. 进入 **「事件订阅」** 页面
2. 开启 **「启用事件订阅」**
3. 填写 **请求网址**（需要公网可访问）：
   ```
   https://your-domain.com/feishu/webhook
   ```
4. 订阅以下事件：
   - `im.message.receive_v1` - 接收消息
   - `im.chat.member.single_chat.enter_v1` - 用户进入单聊

5. 点击 **「保存」**

### 第 5 步：发布应用

1. 进入 **「版本管理与发布」**
2. 点击 **「创建版本」**
3. 填写版本信息
4. 提交审核（个人使用可跳过）
5. 点击 **「发布」**

### 第 6 步：添加到飞书

1. 在飞书客户端左侧栏找到 **「应用」**
2. 搜索你创建的应用名称
3. 点击添加
4. 可以私聊机器人，或添加到群聊

---

## 💻 方案三：Python 对接脚本

创建一个简单的 Python 脚本来对接飞书：

### 安装依赖

```bash
pip install requests flask
```

### 创建飞书机器人脚本

```python
# feishu_bot.py
import requests
import json
from flask import Flask, request

app = Flask(__name__)

# 飞书 Webhook 地址（替换成你的）
WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/你的 webhook 地址"

# 发送文本消息
def send_text_message(text):
    data = {
        "msg_type": "text",
        "content": {
            "text": text
        }
    }
    response = requests.post(WEBHOOK_URL, json=data)
    return response.json()

# 发送富文本卡片消息
def send_card_message(title, content, buttons=None):
    card = {
        "msg_type": "interactive",
        "card": {
            "header": {
                "title": {
                    "tag": "plain_text",
                    "content": title
                },
                "template": "blue"
            },
            "elements": [
                {
                    "tag": "markdown",
                    "content": content
                }
            ]
        }
    }
    
    if buttons:
        card["card"]["elements"].append({
            "tag": "action",
            "actions": buttons
        })
    
    response = requests.post(WEBHOOK_URL, json=card)
    return response.json()

# 测试
if __name__ == "__main__":
    # 发送测试消息
    send_text_message("你好，我是律师助手！⚖️")
    
    # 发送卡片消息
    send_card_message(
        title="⚖️ 律师工具箱",
        content="**可用工具：**\n- 💰 诉讼费计算器\n- 📈 利息计算器\n- 📄 法律文书生成\n- 📁 案件管理\n\n访问本地网站使用完整功能！",
        buttons=[{
            "tag": "button",
            "text": {"tag": "plain_text", "content": "打开工具箱"},
            "url": "http://localhost:8080",
            "type": "primary"
        }]
    )
    
    print("消息已发送！")
```

### 运行脚本

```bash
python feishu_bot.py
```

---

## 🌐 方案四：部署到云端（公网访问）

如果需要飞书回调到你的服务器，需要公网地址：

### 使用 Vercel 部署（免费）

1. 安装 Vercel CLI：
   ```bash
   npm install -g vercel
   ```

2. 创建 `api/feishu.js`：
   ```javascript
   export default async function handler(req, res) {
     if (req.method === 'POST') {
       const { challenge, type, ...event } = req.body;
       
       // 验证 URL
       if (type === 'url_verification') {
         return res.status(200).json({ challenge });
       }
       
       // 处理消息
       console.log('收到消息:', event);
       
       return res.status(200).json({ success: true });
     }
     
     return res.status(405).json({ error: 'Method not allowed' });
   }
   ```

3. 部署：
   ```bash
   vercel
   ```

4. 获得公网地址，填入飞书事件订阅

---

## 📋 快速检查清单

- [ ] 创建飞书账号（如有可跳过）
- [ ] 访问飞书开放平台 open.feishu.cn
- [ ] 创建机器人或自建应用
- [ ] 复制 Webhook 地址或 App ID/Secret
- [ ] 配置权限
- [ ] 测试消息发送
- [ ] 添加到群聊或私聊
- [ ] （可选）部署到云端

---

## 🔗 相关资源

- 飞书开放平台：https://open.feishu.cn/
- 飞书机器人文档：https://open.feishu.cn/document/ukTMukTMukTM/ucTM5YjL3ETO24yNxkjN
- 飞书 API 探索工具：https://open.feishu.cn/tool
- 飞书开发者社区：https://open.feishu.cn/community

---

## 💡 需要帮助？

如果你告诉我：
1. 你是个人使用还是团队使用？
2. 需要哪些具体功能？（消息通知/交互式工具/文件处理）
3. 有公网服务器吗？

我可以给你更具体的对接方案！
