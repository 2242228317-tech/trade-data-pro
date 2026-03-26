# TradeData Pro 会员系统集成指南

## 📁 已创建的文件

### 后端 (Backend)
```
backend/
├── app/
│   ├── models/
│   │   └── membership.py      # 用户、支付、会员等级模型
│   ├── core/
│   │   └── auth.py            # JWT认证、权限检查依赖
│   └── api/
│       └── membership.py      # 会员相关API路由
```

### 前端 (Frontend)
```
frontend/
├── app/
│   └── pricing/
│       └── page.tsx           # 定价页面
└── components/
    ├── UpgradePrompt.tsx      # 升级提示组件（Badge/Card/Modal/Quota/Export按钮）
    └── MembershipEntry.tsx    # 会员入口组件（浮动按钮/导航入口/遮罩）
```

---

## 🔧 集成步骤

### 步骤 1: 更新数据库

```python
# 在 backend/app/models/database.py 中添加
from models.membership import User, Payment

# 然后运行迁移（或使用 alembic）
```

### 步骤 2: 注册路由

```python
# 在 backend/app/main.py 中添加
from api.membership import router as membership_router

app.include_router(membership_router)
```

### 步骤 3: 安装依赖

```bash
cd backend
pip install python-jose[cryptography] passlib[bcrypt]
```

---

## 💡 使用示例

### 1. 保护API接口（后端）

```python
from fastapi import APIRouter, Depends
from core.auth import (
    get_current_user,           # 获取当前用户
    check_query_quota,          # 检查查询配额
    require_minimum_role,       # 要求最低会员等级
    require_export_permission,  # 要求导出权限
    require_api_access          # 要求API访问权限
)
from models.membership import UserRole

router = APIRouter()

# 基础查询接口 - 检查配额
@router.get("/products/search")
def search_products(
    q: str,
    user = Depends(check_query_quota)  # 自动检查并扣除配额
):
    return {"results": [], "remaining": user.daily_query_limit - user.daily_queries_used}

# 导出接口 - 需要导出权限
@router.post("/products/export")
def export_products(
    user = Depends(require_export_permission)
):
    return {"download_url": "..."}

# API接口 - 需要专业版
@router.get("/api/v1/data")
def api_data(
    user = Depends(require_minimum_role(UserRole.PRO))
):
    return {"data": []}

# 企业版功能
@router.get("/admin/analytics")
def admin_analytics(
    user = Depends(require_minimum_role(UserRole.ENTERPRISE))
):
    return {"analytics": []}
```

### 2. 前端使用升级提示

```tsx
// 在 page.tsx 中引入
import { 
  UpgradeBadge,      // 小型标签
  UpgradeCard,       // 卡片形式
  UpgradeModal,      // 弹窗形式
  QuotaIndicator,    // 配额指示器
  ExportButton       // 导出按钮（自动检查权限）
} from '@/components/UpgradePrompt';

import {
  MembershipFloatButton,   // 右下角浮动按钮
  NavbarMembershipEntry,   // 导航栏入口
  PremiumOverlay           // 内容遮罩
} from '@/components/MembershipEntry';

// === 使用示例 ===

// 1. 在功能受限处显示升级徽章
<div className="flex items-center gap-2">
  <span>数据导出</span>
  <UpgradeBadge requiredPlan="basic" />
</div>

// 2. 在页面中显示升级卡片
<UpgradeCard
  feature="数据导出"
  description="将查询结果导出为 Excel 格式，方便离线分析和报告制作。"
  requiredPlan="basic"
/>

// 3. 显示配额使用情况
<QuotaIndicator 
  used={8} 
  limit={10} 
  resetAt="2024-03-23T00:00:00Z"
/>

// 4. 导出按钮（自动处理权限检查）
<ExportButton 
  onClick={() => doExport()}
  hasPermission={user.can_export}
  requiredPlan="basic"
/>

// 5. 浮动会员入口（添加到 layout.tsx）
<MembershipFloatButton />

// 6. 导航栏入口
<NavbarMembershipEntry />

// 7. 内容遮罩（预览付费内容）
<PremiumOverlay requiredPlan="pro" feature="历史趋势分析">
  <Chart data={premiumData} />
</PremiumOverlay>
```

### 3. 修改现有首页添加会员元素

```tsx
// 在 frontend/app/page.tsx 中添加

import { MembershipFloatButton, NavbarMembershipEntry } from '@/components/MembershipEntry';
import { QuotaIndicator, ExportButton } from '@/components/UpgradePrompt';

// 在 Navbar 组件中添加会员入口
function Navbar() {
  return (
    <nav>...</nav>
    // ... 现有代码 ...
    
    // 在导航链接后添加
    <NavbarMembershipEntry />
  );
}

// 在页面底部添加浮动按钮
export default function Home() {
  return (
    <div>
      {/* 现有内容 */}
      
      {/* 会员浮动入口 */}
      <MembershipFloatButton />
    </div>
  );
}
```

---

## 💰 支付接入

### 支付宝接入

```python
# 安装 SDK
pip install alipay-sdk-python

# 在 membership.py 中实现
def create_alipay_order(order_id: str, amount: float, subject: str):
    from alipay import AliPay
    
    alipay = AliPay(
        appid="your-app-id",
        app_notify_url="https://your-domain.com/api/v1/membership/payment/notify/alipay",
        app_private_key_string="your-private-key",
        alipay_public_key_string="alipay-public-key",
        sign_type="RSA2",
        debug=False
    )
    
    # 创建订单
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_id,
        total_amount=str(amount),
        subject=subject,
        return_url="https://your-domain.com/payment/success",
        notify_url="https://your-domain.com/api/v1/membership/payment/notify/alipay"
    )
    
    return f"https://openapi.alipay.com/gateway.do?{order_string}"
```

### 微信支付接入

```python
pip install wechatpayv3

# 类似方式实现...
```

### Stripe 接入（国际）

```python
pip install stripe

import stripe
stripe.api_key = "sk_test_..."

def create_stripe_session(order_id: str, amount: float, plan_name: str):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': f'TradeData Pro - {plan_name}'},
                'unit_amount': int(amount * 100),  # 转换为分
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://your-domain.com/payment/success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='https://your-domain.com/pricing',
        metadata={'order_id': order_id}
    )
    return session.url
```

---

## 🎯 变现策略建议

### 1. 免费层 (Freemium)
- 每日 10 次查询
- 最近 3 个月数据
- 基础图表
- **目标**: 让用户感受到产品价值

### 2. 基础版 (¥29/月)
- 每日 100 次查询
- 最近 12 个月数据
- CSV 导出
- **目标**: 个人研究者、学生

### 3. 专业版 (¥99/月) ⭐ 主推
- 无限查询
- 5 年历史数据
- Excel + API 访问
- **目标**: 专业分析师、交易员

### 4. 企业版 (¥299/月)
- 无限查询
- 10 年历史数据
- 批量导出 + 数据推送
- 专属客服
- **目标**: 企业数据部门

---

## 📊 监控指标

建议跟踪以下指标：

1. **转化率**: 免费用户 → 付费用户
2. **流失率**: 取消订阅的比例
3. **LTV**: 用户生命周期价值
4. **MRR**: 月经常性收入
5. **功能使用率**: 哪些付费功能最受欢迎

---

## ⚠️ 注意事项

1. **支付安全**: 生产环境务必使用 HTTPS，妥善保管密钥
2. **税务合规**: 收入需要申报，建议接入自动开票系统
3. **退款政策**: 明确退款规则，避免纠纷
4. **数据隐私**: 用户信息加密存储，遵守相关法规

---

## 🚀 快速启动

```bash
# 1. 进入项目目录
cd trade-data-pro

# 2. 启动后端
cd backend
pip install -r requirements.txt
# 添加 python-jose 和 passlib 到 requirements.txt
uvicorn app.main:app --reload

# 3. 启动前端
cd ../frontend
npm install
npm run dev

# 4. 访问定价页面
open http://localhost:3000/pricing
```

---

## 📞 需要帮助？

如有问题，可以：
1. 查看代码注释
2. 参考 FastAPI 官方文档
3. 查看各支付平台的开发者文档
