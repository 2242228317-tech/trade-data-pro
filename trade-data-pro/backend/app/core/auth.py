from datetime import datetime, timedelta
from functools import wraps
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from app.models.database import get_db
from app.models.membership import User, UserRole, MEMBERSHIP_PLANS

# JWT配置（生产环境用环境变量）
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"

security = HTTPBearer()

def create_access_token(user_id: int) -> str:
    """创建JWT令牌"""
    to_encode = {"sub": str(user_id), "type": "access"}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """获取当前登录用户"""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证令牌"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在"
        )
    
    # 检查会员是否过期
    if user.subscription_expires_at and user.subscription_expires_at < datetime.utcnow():
        if user.role != UserRole.FREE:
            user.role = UserRole.FREE
            user.subscription_status = "expired"
            # 重置权限为免费版
            plan = MEMBERSHIP_PLANS[UserRole.FREE]
            user.daily_query_limit = plan["daily_queries"]
            user.data_months_limit = plan["data_months"]
            user.can_export = plan["can_export"]
            user.can_api_access = plan["can_api"]
            db.commit()
    
    # 检查是否需要重置每日配额
    from datetime import timedelta
    if user.last_query_reset and (datetime.utcnow() - user.last_query_reset) > timedelta(days=1):
        user.daily_queries_used = 0
        user.last_query_reset = datetime.utcnow()
        db.commit()
    
    return user

def check_query_quota(user: User = Depends(get_current_user)):
    """检查查询配额"""
    if user.daily_queries_used >= user.daily_query_limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "message": "今日查询次数已用完",
                "used": user.daily_queries_used,
                "limit": user.daily_query_limit,
                "reset_at": (user.last_query_reset + timedelta(days=1)).isoformat() if user.last_query_reset else None,
                "upgrade_url": "/pricing"
            }
        )
    
    # 增加已用次数
    user.daily_queries_used += 1
    return user

def require_minimum_role(min_role: str):
    """要求最低会员等级"""
    role_hierarchy = ["free", "basic", "pro", "enterprise"]
    min_index = role_hierarchy.index(min_role)
    
    def checker(user: User = Depends(get_current_user)) -> User:
        user_index = role_hierarchy.index(user.role) if user.role in role_hierarchy else 0
        if user_index < min_index:
            plan_info = MEMBERSHIP_PLANS.get(min_role, {})
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "message": f"需要 {plan_info.get('name', min_role)} 或更高等级",
                    "current_role": user.role,
                    "required_role": min_role,
                    "upgrade_url": "/pricing"
                }
            )
        return user
    return checker

def require_export_permission(user: User = Depends(get_current_user)) -> User:
    """要求导出权限"""
    if not user.can_export:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": "导出功能需要付费会员",
                "upgrade_url": "/pricing",
                "suggested_plan": "BASIC"
            }
        )
    return user

def require_api_access(user: User = Depends(get_current_user)) -> User:
    """要求API访问权限"""
    if not user.can_api_access:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": "API访问需要专业版会员",
                "upgrade_url": "/pricing",
                "suggested_plan": "PRO"
            }
        )
    return user

def get_user_limits(user: User) -> dict:
    """获取用户当前限制状态"""
    # 将字符串 role 转换为 UserRole 枚举来获取配置
    role_mapping = {
        "free": UserRole.FREE,
        "basic": UserRole.BASIC,
        "pro": UserRole.PRO,
        "enterprise": UserRole.ENTERPRISE
    }
    user_role = role_mapping.get(user.role, UserRole.FREE)
    plan = MEMBERSHIP_PLANS.get(user_role, MEMBERSHIP_PLANS[UserRole.FREE])
    
    return {
        "role": user.role,
        "role_name": plan["name"],
        "queries": {
            "used": user.daily_queries_used,
            "limit": user.daily_query_limit,
            "remaining": max(0, user.daily_query_limit - user.daily_queries_used),
            "reset_at": (user.last_query_reset + timedelta(days=1)).isoformat() if user.last_query_reset else None
        },
        "data_access": {
            "months": user.data_months_limit,
            "can_export": user.can_export,
            "can_api": user.can_api_access
        },
        "subscription": {
            "status": user.subscription_status,
            "expires_at": user.subscription_expires_at.isoformat() if user.subscription_expires_at else None,
            "is_active": user.subscription_expires_at > datetime.utcnow() if user.subscription_expires_at else user.role == "free"
        }
    }
