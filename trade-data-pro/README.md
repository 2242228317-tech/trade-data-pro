# TradeData Pro - 上线部署指南

## 📋 项目概述

TradeData Pro 是一个专业的外贸出口商品数据分析平台，提供1688商品数据和海关统计数据查询。

## 🚀 快速上线步骤（推荐）

### 方案A：使用 Render + Vercel（免费，推荐）

#### 1. 准备工作

```bash
# 1. 确保代码已提交到GitHub
git add .
git commit -m "准备生产部署 v1.0"
git push origin main
```

#### 2. 部署后端到 Render

1. 访问 https://dashboard.render.com/
2. 点击 **New +** → **PostgreSQL**
   - Name: `tradedata-db`
   - Database: `tradedata`
   - User: `tradedata`
   - 点击 **Create Database**
   - 复制 **Internal Database URL**

3. 点击 **New +** → **Web Service**
   - 连接你的 GitHub 仓库
   - Name: `tradedata-api`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. 点击 **Advanced** → **Environment Variables**，添加：
   ```
   DATABASE_URL = postgresql://tradedata:xxx@postgres:5432/tradedata  (从上面复制)
   SECRET_KEY =  openssl rand -hex 32 生成的密钥
   ADMIN_KEY =  你的管理员密码（不要用trade888）
   FRONTEND_URL = https://你的前端域名.vercel.app
   DEBUG = false
   ```

5. 点击 **Create Web Service**

#### 3. 部署前端到 Vercel

1. 访问 https://vercel.com/
2. 导入同一个 GitHub 仓库
3. 配置：
   - Framework Preset: Next.js
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `.next`
4. 添加环境变量：
   ```
   NEXT_PUBLIC_API_URL = https://tradedata-api.onrender.com/api
   ```
5. 点击 Deploy

#### 4. 初始化数据

```bash
# 本地运行数据初始化脚本
python init_data.py
```

或者通过 Render Shell：
```bash
cd backend && python -c "from app.models.database import init_db; init_db()"
```

#### 5. 配置支付收款码

1. 上传你的收款码到 `frontend/public/images/`
   - 支付宝：`alipay-qr.png`
   - 微信：`wechat-qr.png`

2. 重新部署前端

---

### 方案B：本地服务器部署

如果你有云服务器（阿里云/腾讯云/AWS）：

```bash
# 1. 克隆代码
git clone <your-repo>

# 2. 安装依赖
cd trade-data-pro
pip install -r backend/requirements.txt
cd frontend && npm install && cd ..

# 3. 配置环境变量
cp backend/.env.example backend/.env
# 编辑 .env 填入配置

# 4. 初始化数据库
python init_data.py

# 5. 使用 PM2 启动
npm install -g pm2
pm2 start backend/app/main.py --name tradedata-api --interpreter python
cd frontend && pm2 start npm --name tradedata-web -- run start
```

---

## 💳 支付配置

### 当前：手动确认模式

优点：
- ✅ 无需企业资质
- ✅ 快速启动
- ✅ 手续费低

缺点：
- ⚠️ 需要人工确认订单
- ⚠️ 用户体验略差

**配置步骤：**
1. 准备个人收款码（支付宝/微信）
2. 将收款码放入 `frontend/public/images/`
3. 在用户付款后24小时内，访问管理后台确认：
   ```
   https://你的域名/api/manual/membership/admin/payments/pending?admin_key=你的密钥
   ```

### 升级：自动支付（可选）

| 平台 | 个人可用 | 手续费 | 接入难度 |
|------|---------|--------|---------|
| Stripe | ✅（需护照） | 3% | 简单 |
| Paddle | ✅ | 5%+0.5$ | 简单 |
| 微信支付 | ❌（需企业） | 0.6% | 中等 |
| 支付宝 | ❌（需企业） | 0.6% | 中等 |

---

## 🔒 安全检查清单

部署前请确认：

- [ ] 修改 `SECRET_KEY`（不要用默认值）
- [ ] 修改 `ADMIN_KEY`（不要用 trade888）
- [ ] 配置正确的 `FRONTEND_URL`（CORS安全）
- [ ] 启用 HTTPS（Render/Vercel自动提供）
- [ ] 删除测试账号和数据
- [ ] 配置数据库备份

---

## 📊 运营建议

### 定价策略

| 套餐 | 价格 | 推荐人群 |
|------|------|---------|
| 免费版 | ¥0 | 个人体验 |
| 基础版 | ¥29/月 | 个人研究者 |
| 专业版 | ¥99/月 | 专业分析师 |
| 企业版 | ¥299/月 | 企业数据部门 |

### 推广渠道

1. **小红书/抖音** - 外贸相关内容引流
2. **知乎/公众号** - 干货文章植入
3. **外贸社群** - 免费体验码推广
4. **SEO** - 海关数据、选品工具等关键词

---

## 💰 成本估算

| 项目 | Render免费版 | Render付费版 |
|------|-------------|--------------|
| 前端托管(Vercel) | ¥0 | ¥0 |
| 后端托管 | ¥0 | ~¥50/月 |
| 数据库(PostgreSQL) | ¥0 | ~¥100/月 |
| 域名 | ~¥70/年 | ~¥70/年 |
| **首年总计** | **¥70** | **约¥2000** |

---

## 🐛 常见问题

### Q: Render免费版会休眠？
A: 是的，15分钟无访问会休眠，首次访问需等待10-30秒唤醒。可配置定时ping保持活跃。

### Q: 数据如何备份？
A: Render PostgreSQL提供自动备份。也可定期导出：
```bash
pg_dump $DATABASE_URL > backup.sql
```

### Q: 如何修改收款码？
```bash
# 替换 frontend/public/images/ 下的图片
# 重新部署前端
git add .
git commit -m "更新收款码"
git push
# Vercel会自动重新部署
```

---

## 📞 技术支持

遇到问题？
1. 查看 Render 日志：Dashboard → Web Service → Logs
2. 查看 Vercel 日志：Dashboard → Project → Functions
3. API 测试：访问 `/docs` 查看 Swagger 文档

---

**祝你上线顺利，生意兴隆！** 🎉
