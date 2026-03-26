"""
会员和支付相关API
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid
import hashlib

from app.models.database import get_db
from app.models.membership import User, Payment, UserRole, SubscriptionStatus, MEMBERSHIP_PLANS
from app.core.auth import get_current_user, get_user_limits

router = APIRouter(prefix="/membership", tags=["membership"])

# ============ 数据模型 ============

class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

class PricingPlan(BaseModel):
    role: str
    name: str
    price_cny: float
    price_usd: float
    features: dict
    description: str

class CreatePaymentRequest(BaseModel):
    plan: str  # free/basic/pro/enterprise
    duration_months: int = 1
    payment_method: str  # alipay / wechat / stripe

class PaymentResponse(BaseModel):
    order_id: str
    payment_url: Optional[str] = None
    qr_code: Optional[str] = None  # base64二维码
    status: str

# ============ 认证接口 ============

@router.post("/auth/register", response_model=TokenResponse)
def register(data: UserRegister, db: Session = Depends(get_db)):
    """用户注册"""
    # 检查邮箱是否已存在
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="邮箱已注册")
    
    # 使用 SHA256 加密密码（生产环境应使用 bcrypt，但需处理 72 字节限制）
    import hashlib
    hashed_password = hashlib.sha256(data.password.encode()).hexdigest()
    
    user = User(
        email=data.email,
        hashed_password=hashed_password,
        role="free",
        daily_query_limit=MEMBERSHIP_PLANS[UserRole.FREE]["daily_queries"],
        data_months_limit=MEMBERSHIP_PLANS[UserRole.FREE]["data_months"],
        can_export=MEMBERSHIP_PLANS[UserRole.FREE]["can_export"],
        can_api_access=MEMBERSHIP_PLANS[UserRole.FREE]["can_api"]
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # 生成JWT
    from app.core.auth import create_access_token
    token = create_access_token(user.id)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "limits": get_user_limits(user)
        }
    }

@router.post("/auth/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    """用户登录"""
    import hashlib
    hashed_password = hashlib.sha256(data.password.encode()).hexdigest()
    
    user = db.query(User).filter(User.email == data.email).first()
    if not user or user.hashed_password != hashed_password:
        raise HTTPException(status_code=401, detail="邮箱或密码错误")
    
    from app.core.auth import create_access_token
    token = create_access_token(user.id)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "limits": get_user_limits(user)
        }
    }

# ============ 会员信息接口 ============

@router.get("/me")
def get_me(user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return {
        "id": user.id,
        "email": user.email,
        "limits": get_user_limits(user)
    }

@router.get("/pricing", response_model=list[PricingPlan])
def get_pricing():
    """获取会员价格方案"""
    plans = []
    for role, plan in MEMBERSHIP_PLANS.items():
        plans.append(PricingPlan(
            role=role,
            name=plan["name"],
            price_cny=plan["price_cny"],
            price_usd=plan["price_usd"],
            features={
                "daily_queries": plan["daily_queries"],
                "data_months": plan["data_months"],
                "can_export": plan["can_export"],
                "can_api": plan["can_api"]
            },
            description=plan["description"]
        ))
    return plans

# ============ 支付接口 ============

@router.post("/payment/create")
def create_payment(
    data: CreatePaymentRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建支付订单"""
    
    # 验证套餐
    if data.plan not in MEMBERSHIP_PLANS:
        raise HTTPException(status_code=400, detail="无效的套餐")
    
    plan_info = MEMBERSHIP_PLANS[data.plan]
    if plan_info["price_cny"] == 0:
        raise HTTPException(status_code=400, detail="免费套餐无需支付")
    
    # 生成订单号
    order_id = f"TD{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:8].upper()}"
    
    # 计算金额
    amount = plan_info["price_cny"] * data.duration_months
    
    # 创建支付记录
    payment = Payment(
        user_id=user.id,
        amount=amount,
        currency="CNY",
        payment_method=data.payment_method,
        order_id=order_id,
        plan=data.plan,
        duration_months=data.duration_months,
        status="pending"
    )
    db.add(payment)
    db.commit()
    
    # 根据支付方式返回不同的支付信息
    if data.payment_method == "alipay":
        # 实际项目中调用支付宝SDK
        # 这里返回模拟数据
        return {
            "order_id": order_id,
            "payment_url": f"/api/v1/membership/payment/alipay/{order_id}",
            "amount": amount,
            "qr_code": None,  # 实际应该是支付宝返回的二维码
            "status": "pending",
            "expire_at": (datetime.utcnow() + timedelta(minutes=30)).isoformat()
        }
    
    elif data.payment_method == "wechat":
        return {
            "order_id": order_id,
            "payment_url": None,
            "amount": amount,
            "qr_code": "data:image/png;base64,iVBORw0KGgo...",  # 微信支付二维码
            "status": "pending",
            "expire_at": (datetime.utcnow() + timedelta(minutes=30)).isoformat()
        }
    
    elif data.payment_method == "stripe":
        # Stripe Checkout Session
        return {
            "order_id": order_id,
            "payment_url": f"https://checkout.stripe.com/pay/{order_id}",  # 实际是Stripe返回的URL
            "amount": amount,
            "status": "pending"
        }
    
    raise HTTPException(status_code=400, detail="不支持的支付方式")

@router.post("/payment/notify/{payment_method}")
def payment_notify(
    payment_method: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """
    支付回调通知
    支付宝/微信/Stripe 支付成功后回调此接口
    """
    # 实际项目中需要验证签名
    # 这里简化处理
    
    body = request.json()
    order_id = body.get("order_id") or body.get("out_trade_no")
    
    payment = db.query(Payment).filter(Payment.order_id == order_id).first()
    if not payment:
        return {"status": "fail", "message": "订单不存在"}
    
    if payment.status == "paid":
        return {"status": "success"}
    
    # 更新支付状态
    payment.status = "paid"
    payment.paid_at = datetime.utcnow()
    payment.transaction_id = body.get("trade_no") or body.get("transaction_id")
    
    # 更新用户会员等级
    user = db.query(User).filter(User.id == payment.user_id).first()
    
    # 如果用户当前是免费或更低等级，或已过期，则更新
    role_hierarchy = ["free", "basic", "pro", "enterprise"]
    current_index = role_hierarchy.index(user.role) if user.role in role_hierarchy else 0
    new_index = role_hierarchy.index(payment.plan) if payment.plan in role_hierarchy else 0
    
    if new_index > current_index or (user.subscription_expires_at and user.subscription_expires_at < datetime.utcnow()):
        user.role = payment.plan
        user.subscription_status = "active"
        
        # 计算到期时间
        if user.subscription_expires_at and user.subscription_expires_at > datetime.utcnow():
            # 续费：在当前到期时间上累加
            user.subscription_expires_at = user.subscription_expires_at + timedelta(days=30*payment.duration_months)
        else:
            # 新购：从当前时间算起
            user.subscription_expires_at = datetime.utcnow() + timedelta(days=30*payment.duration_months)
        
        # 更新权限
        plan_key = payment.plan.upper()
        if hasattr(UserRole, plan_key):
            plan = MEMBERSHIP_PLANS[getattr(UserRole, plan_key)]
            user.daily_query_limit = plan["daily_queries"]
            user.data_months_limit = plan["data_months"]
            user.can_export = plan["can_export"]
            user.can_api_access = plan["can_api"]
    
    db.commit()
    
    return {"status": "success"}

@router.get("/payment/status/{order_id}")
def get_payment_status(
    order_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """查询支付状态"""
    payment = db.query(Payment).filter(
        Payment.order_id == order_id,
        Payment.user_id == user.id
    ).first()
    
    if not payment:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    return {
        "order_id": payment.order_id,
        "amount": payment.amount,
        "status": payment.status,
        "plan": payment.plan.value,
        "duration_months": payment.duration_months,
        "paid_at": payment.paid_at.isoformat() if payment.paid_at else None,
        "created_at": payment.created_at.isoformat()
    }

@router.get("/payments/history")
def get_payment_history(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取支付历史"""
    payments = db.query(Payment).filter(
        Payment.user_id == user.id
    ).order_by(Payment.created_at.desc()).all()
    
    return [
        {
            "order_id": p.order_id,
            "amount": p.amount,
            "plan": p.plan.value,
            "status": p.status,
            "paid_at": p.paid_at.isoformat() if p.paid_at else None,
            "created_at": p.created_at.isoformat()
        }
        for p in payments
    ]
