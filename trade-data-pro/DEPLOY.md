# TradeData Pro 生产部署指南

## 快速部署步骤（30分钟内上线）

### 1. 准备代码

```bash
# 确保所有修改已提交
git add .
git commit -m "准备生产部署"
git push origin main
```

### 2. 部署后端到 Render

#### 2.1 创建 PostgreSQL 数据库
1. 访问 https://dashboard.render.com/
2. 点击 "New +" → "PostgreSQL"
3. 配置：
   - Name: `tradedata-db`
   - Database: `tradedata`
   - User: `tradedata`
   - 其他保持默认
4. 点击 "Create Database"
5. 复制 **Internal Database URL**（后续用）

#### 2.2 创建 Web Service
1. 点击 "New +" → "Web Service"
2. 连接你的 GitHub 仓库
3. 配置：
   - Name: `tradedata-api`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`
4. 点击 "Advanced" 添加环境变量：
   ```
   DATABASE_URL = postgresql://tradedata:xxx@postgres:5432/tradedata  # 从上一步复制
   SECRET_KEY = your-256-bit-secret-key  # 生成: openssl rand -hex 32
   ADMIN_KEY = your-admin-key-2024  # 管理后台密码
   DEBUG = false
   ```
5. 点击 "Create Web Service"

### 3. 部署前端到 Vercel

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

### 4. 配置支付（分阶段）

#### 阶段A：手动确认（快速启动，适合测试）
- 使用现有的 `manual_payment.py`
- 配置个人收款码
- 管理员手动确认订单

#### 阶段B：自动支付（正式运营）
需要企业资质：
- 微信支付商户号（需营业执照）
- 支付宝企业账号

替代方案（无需企业资质）：
- **Stripe**（支持国内个人，需护照）
- **Paddle**（支持个人开发者）
- **LemonSqueezy**（支持个人）

### 5. 初始化数据

```bash
# 连接到 Render 数据库
render psql tradedata-db

# 或者通过后端API初始化
# 部署后访问: https://tradedata-api.onrender.com/docs
```

## 生产检查清单

### 安全
- [ ] 修改 SECRET_KEY（不要用默认值）
- [ ] 修改 ADMIN_KEY（不要用 trade888）
- [ ] 开启 HTTPS（Render/Vercel 自动提供）
- [ ] 配置 CORS 白名单（不要允许 *）

### 性能
- [ ] 配置数据库连接池
- [ ] 添加 Redis 缓存（可选）
- [ ] 配置 CDN（Vercel 自动提供）

### 监控
- [ ] 配置日志收集
- [ ] 设置健康检查
- [ ] 配置告警（Render 有内置监控）

## 域名配置

### 方法1：Vercel 自带域名（免费）
- 自动获得 `xxx.vercel.app` 域名

### 方法2：自定义域名
1. 购买域名（阿里云/腾讯云/GoDaddy）
2. 在 Vercel 添加自定义域名
3. 在域名服务商添加 CNAME 记录

## 成本估算

| 项目 | 免费版 | 付费版（推荐） |
|------|--------|----------------|
| 前端托管(Vercel) | $0 | $0 |
| 后端托管(Render) | $0 | $7/月 |
| 数据库(Render) | $0 | $0-15/月 |
| 域名 | - | ¥70/年 |
| **总计** | **免费** | **约¥150/月** |

## 扩展建议

当用户量增长后：
1. 数据库升级到 AWS RDS 或阿里云 RDS
2. 后端迁移到阿里云 ECS 或 AWS EC2
3. 添加 Redis 缓存（Render Redis 或 Upstash）
4. 使用 CDN 加速静态资源

## 紧急回滚

如果部署出问题：
```bash
# 在 Render Dashboard 中
# 1. 找到 Web Service
# 2. 点击 "Manual Deploy" → "Deploy latest commit"
# 3. 或者 "Rollback" 到上一个版本
```
