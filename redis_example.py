import redis

# 连接到Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# 存储会话数据
def store_session(session_id, user_data):
    r.hmset(f"session:{session_id}", user_data)
    r.expire(f"session:{session_id}", 3600)  # 设置1小时过期

# 获取会话数据
def get_session(session_id):
    return r.hgetall(f"session:{session_id}")

# 使用示例
store_session("user123", {"username": "john_doe", "last_login": "2023-05-01"})
user_data = get_session("user123")
print(user_data)