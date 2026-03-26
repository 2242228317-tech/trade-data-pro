"""
手动确认支付系统 - 生产版本
用户付款到个人账号，管理员手动确认
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
import uuid

from app.models.database import get_db, User, Payment
from app.core.config import settings

router = APIRouter(prefix="/membership", tags=["membership"])

# 会员配置
MEMBERSHIP_PLANS = {
    "free": {"name": "免费版", "price_cny": 0},
    "basic": {"name": "基础版", "price_cny": 29, "daily_queries": 100, "data_months": 12, "can_export": True, "can_api": False},
    "pro": {"name": "专业版", "price_cny": 99, "daily_queries": 999999, "data_months": 60, "can_export": True, "can_api": True},
    "enterprise": {"name": "企业版", "price_cny": 299, "daily_queries": 999999, "data_months": 120, "can_export": True, "can_api": True}
}

# 支付配置
MANUAL_PAYMENT_CONFIG = {
    "alipay": {
        "enabled": True,
        "name": "支付宝",
        "account": "管理员",
        "qr_code_url": "/images/alipay-qr.png",
        "note_template": "TradeData-{order_id}"
    },
    "wechat": {
        "enabled": True, 
        "name": "微信支付",
        "account": "管理员",
        "qr_code_url": "/images/wechat-qr.png",
        "note_template": "TradeData-{order_id}"
    }
}

# ============ 数据模型 ============

class CreateManualPaymentRequest(BaseModel):
    plan: str
    duration_months: int = 1
    payment_method: str

class ManualPaymentResponse(BaseModel):
    order_id: str
    amount: float
    payment_method: str
    qr_code_url: str
    account_info: str
    note: str
    status: str
    expires_at: str

class ConfirmPaymentRequest(BaseModel):
    order_id: str
    confirm: bool
    admin_notes: Optional[str] = None

# ============ 辅助函数 ============

def get_current_user_from_token(authorization: str = "", db: Session = Depends(get_db)) -> User:
    """从Authorization头获取当前用户"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="请先登录")
    
    token = authorization.replace("Bearer ", "")
    
    # 解码JWT
    from jose import jwt, JWTError
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="无效的认证凭据")
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")
    
    return user

# ============ 用户接口 ============

@router.post("/payment/manual/create", response_model=ManualPaymentResponse)
def create_manual_payment(
    data: CreateManualPaymentRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    """创建手动支付订单"""
    # 获取当前用户
    auth_header = request.headers.get("Authorization", "")
    user = get_current_user_from_token(auth_header, db)
    
    # 验证套餐
    valid_plans = ["basic", "pro", "enterprise"]
    if data.plan not in valid_plans:
        raise HTTPException(status_code=400, detail="无效的套餐")
    
    plan_info = MEMBERSHIP_PLANS[data.plan]
    if plan_info["price_cny"] == 0:
        raise HTTPException(status_code=400, detail="免费套餐无需支付")
    
    # 检查支付方式
    if data.payment_method not in MANUAL_PAYMENT_CONFIG:
        raise HTTPException(status_code=400, detail="不支持的支付方式")
    
    config = MANUAL_PAYMENT_CONFIG[data.payment_method]
    if not config["enabled"]:
        raise HTTPException(status_code=400, detail="该支付方式暂不可用")
    
    # 生成订单号
    order_id = f"TD{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:6].upper()}"
    
    # 计算金额
    amount = plan_info["price_cny"] * data.duration_months
    
    # 创建支付记录
    payment = Payment(
        user_id=user.id,
        amount=amount,
        currency="CNY",
        payment_method=f"manual_{data.payment_method}",
        order_id=order_id,
        plan=data.plan,
        duration_months=data.duration_months,
        status="pending_manual",
        metadata_json=f'{{"user_email": "{user.email}", "note": "{config["note_template"].format(order_id=order_id)}"}}'
    )
    db.add(payment)
    db.commit()
    
    return ManualPaymentResponse(
        order_id=order_id,
        amount=amount,
        payment_method=config["name"],
        qr_code_url=config["qr_code_url"],
        account_info=config["account"],
        note=config["note_template"].format(order_id=order_id),
        status="pending_manual",
        expires_at=(datetime.utcnow() + timedelta(hours=24)).isoformat()
    )

@router.get("/payment/manual/status/{order_id}")
def get_manual_payment_status(
    order_id: str,
    request: Request,
    db: Session = Depends(get_db)
):
    """查询手动支付订单状态"""
    auth_header = request.headers.get("Authorization", "")
    user = get_current_user_from_token(auth_header, db)
    
    payment = db.query(Payment).filter(
        Payment.order_id == order_id,
        Payment.user_id == user.id
    ).first()
    
    if not payment:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    return {
        "order_id": payment.order_id,
        "amount": payment.amount,
        "plan": payment.plan,
        "status": payment.status,
        "created_at": payment.created_at.isoformat(),
        "paid_at": payment.paid_at.isoformat() if payment.paid_at else None,
        "can_retry": payment.status in ["pending_manual", "rejected"]
    }

# ============ 管理员接口 ============

@router.get("/admin/payments/pending")
def get_pending_payments(
    admin_key: str,
    db: Session = Depends(get_db)
):
    """获取待确认的支付订单（管理员用）"""
    if admin_key != settings.ADMIN_KEY:
        raise HTTPException(status_code=403, detail="无权访问")
    
    payments = db.query(Payment).filter(
        Payment.status == "pending_manual"
    ).order_by(Payment.created_at.desc()).all()
    
    return {
        "count": len(payments),
        "payments": [
            {
                "order_id": p.order_id,
                "amount": p.amount,
                "plan": p.plan,
                "duration_months": p.duration_months,
                "payment_method": p.payment_method,
                "user": {
                    "id": p.user.id,
                    "email": p.user.email,
                    "name": p.user.name
                },
                "created_at": p.created_at.isoformat(),
                "note": f"TradeData-{p.order_id}"
            }
            for p in payments
        ]
    }

@router.post("/admin/payments/confirm")
def confirm_manual_payment(
    data: ConfirmPaymentRequest,
    admin_key: str,
    db: Session = Depends(get_db)
):
    """确认或拒绝手动支付（管理员用）"""
    if admin_key != settings.ADMIN_KEY:
        raise HTTPException(status_code=403, detail="无权访问")
    
    payment = db.query(Payment).filter(Payment.order_id == data.order_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    if payment.status != "pending_manual":
        raise HTTPException(status_code=400, detail="订单状态不正确")
    
    if data.confirm:
        # 确认收款，开通会员
        payment.status = "paid"
        payment.paid_at = datetime.utcnow()
        
        # 更新用户会员
        user = db.query(User).filter(User.id == payment.user_id).first()
        user.role = payment.plan
        user.subscription_status = "active"
        
        # 计算到期时间
        if user.subscription_expires_at and user.subscription_expires_at > datetime.utcnow():
            user.subscription_expires_at += timedelta(days=30 * payment.duration_months)
        else:
            user.subscription_expires_at = datetime.utcnow() + timedelta(days=30 * payment.duration_months)
        
        # 更新权限
        plan_info = MEMBERSHIP_PLANS.get(payment.plan, {})
        user.daily_query_limit = plan_info.get("daily_queries", 10)
        user.data_months_limit = plan_info.get("data_months", 3)
        user.can_export = plan_info.get("can_export", False)
        user.can_api_access = plan_info.get("can_api", False)
        
        db.commit()
        
        return {
            "success": True,
            "message": "已确认收款并开通会员",
            "order_id": data.order_id,
            "user_email": user.email,
            "new_role": user.role,
            "expires_at": user.subscription_expires_at.isoformat()
        }
    else:
        # 拒绝收款
        payment.status = "rejected"
        db.commit()
        
        return {
            "success": True,
            "message": "已拒绝订单",
            "order_id": data.order_id,
            "admin_notes": data.admin_notes
        }

@router.get("/admin/dashboard")
def admin_dashboard(
    admin_key: str,
    db: Session = Depends(get_db)
):
    """管理员仪表盘 - 统计数据"""
    if admin_key != settings.ADMIN_KEY:
        raise HTTPException(status_code=403, detail="无权访问")
    
    total_users = db.query(User).count()
    total_payments = db.query(Payment).filter(Payment.status == "paid").count()
    pending_payments = db.query(Payment).filter(Payment.status == "pending_manual").count()
    
    revenue_result = db.query(Payment).filter(Payment.status == "paid").with_entities(Payment.amount).all()
    total_revenue = sum([p[0] for p in revenue_result]) if revenue_result else 0
    
    return {
        "total_users": total_users,
        "total_payments": total_payments,
        "pending_payments": pending_payments,
        "total_revenue": total_revenue,
        "recent_payments": [
            {
                "order_id": p.order_id,
                "amount": p.amount,
                "status": p.status,
                "created_at": p.created_at.isoformat()
            }
            for p in db.query(Payment).order_by(Payment.created_at.desc()).limit(10)
        ]
    }
