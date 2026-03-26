"""
数据库初始化脚本
"""
from app.models.database import engine, Base
from app.models.membership import User, Payment

def init_db():
    """创建所有数据库表"""
    print("正在创建数据库表...")
    Base.metadata.create_all(bind=engine)
    print("数据库表创建完成！")
    
    # 显示创建的表
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"\n已创建的表: {tables}")

if __name__ == "__main__":
    init_db()
