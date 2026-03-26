from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from jose import JWTError, jwt
import hashlib

from app.models.database import get_db, User
from app.core.config import settings

router = APIRouter()

# JWT配置
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"

# 会员配置
MEMBERSHIP_PLANS = {
    "free": {
        "name": "免费版",
        "daily_queries": 10,
        "data_months": 3,
        "can_export": False,
        "can_api": False
    },
    "basic": {
        "name": "基础版",
        "daily_queries": 100,
        "data_months": 12,
        "can_export": True,
        "can_api": False
    },
    "pro": {
        "name": "专业版",
        "daily_queries": 999999,
        "data_months": 60,
        "can_export": True,
        "can_api": True
    },
    "enterprise": {
        "name": "企业版",
        "daily_queries": 999999,
        "data_months": 120,
        "can_export": True,
        "can_api": True
    }
}

# 数据模型
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None
    company: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

def create_access_token(user_id: int) -> str:
    """创建JWT令牌"""
    to_encode = {"sub": str(user_id), "type": "access"}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(lambda x: x), db: Session = Depends(get_db)) -> User:
    """验证JWT并返回当前用户"""
    credentials_exception = HTTPException(
        status_code=401,
        detail="无效的认证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user

def get_user_limits(user: User) -> dict:
    """获取用户当前限制状态"""
    plan = MEMBERSHIP_PLANS.get(user.role, MEMBERSHIP_PLANS["free"])
    
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

# API路由
@router.post("/auth/register", response_model=TokenResponse)
def register(data: UserRegister, db: Session = Depends(get_db)):
    """用户注册"""
    # 检查邮箱是否已存在
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="邮箱已被注册")
    
    # 使用 SHA256 加密密码
    hashed_password = hashlib.sha256(data.password.encode()).hexdigest()
    
    plan = MEMBERSHIP_PLANS["free"]
    user = User(
        email=data.email,
        hashed_password=hashed_password,
        name=data.name,
        company=data.company,
        role="free",
        daily_query_limit=plan["daily_queries"],
        data_months_limit=plan["data_months"],
        can_export=plan["can_export"],
        can_api_access=plan["can_api"]
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # 生成JWT
    token = create_access_token(user.id)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role,
            "limits": get_user_limits(user)
        }
    }

@router.post("/auth/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    """用户登录"""
    hashed_password = hashlib.sha256(data.password.encode()).hexdigest()
    
    user = db.query(User).filter(User.email == data.email).first()
    if not user or user.hashed_password != hashed_password:
        raise HTTPException(status_code=401, detail="邮箱或密码错误")
    
    token = create_access_token(user.id)
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role,
            "limits": get_user_limits(user)
        }
    }

@router.get("/auth/me")
def get_me(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name,
        "company": current_user.company,
        "role": current_user.role,
        "limits": get_user_limits(current_user)
    }
