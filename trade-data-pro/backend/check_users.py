import sqlite3

conn = sqlite3.connect('trade_data.db')
cursor = conn.cursor()

# 查看所有表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("数据库表:", [t[0] for t in tables])

# 查看 users 表结构
cursor.execute("PRAGMA table_info(users)")
columns = cursor.fetchall()
print("\nusers 表结构:")
for col in columns:
    print(f"  {col[1]} ({col[2]})")

# 查看用户表
cursor.execute("SELECT * FROM users ORDER BY id")
users = cursor.fetchall()
print(f"\n共有 {len(users)} 个用户:")
for user in users:
    print(f"  {user}")

conn.close()
