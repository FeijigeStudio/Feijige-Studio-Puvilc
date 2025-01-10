from flask import Flask, render_template, redirect, url_for, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
import redis
import json
import openai

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/feijige_chat'
socketio = SocketIO(app)
db = SQLAlchemy(app)
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# 添加 OpenAI API 密钥
openai.api_key = 'your_openai_api_key'  # 替换为你的实际 OpenAI API 密钥

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# 定时清理聊天记录的函数
def cleanup_old_messages():
    two_days_ago = datetime.utcnow() - timedelta(days=2)
    old_messages = Message.query.filter(Message.timestamp < two_days_ago).all()
    for message in old_messages:
        db.session.delete(message)
    db.session.commit()

# 设置定时任务
scheduler = BackgroundScheduler()
scheduler.add_job(cleanup_old_messages, 'interval', hours=24)  # 每24小时执行一次
scheduler.start()

# 添加登录检查装饰器
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    return render_template('chat_interface.html')

@app.route('/index-logged-in')
@login_required
def index_logged_in():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index-logged-in.html')

@app.route('/login')
def login():
    if 'user_id' in session:
        return redirect(url_for('index_logged_in'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@socketio.on('connect')
def handle_connect():
    if 'user_id' not in session:
        return False  # 拒绝未登录用户的连接

@socketio.on('login')
def handle_login(username):
    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
    join_room(username)
    
    # Cache user info in Redis
    user_info = {'id': user.id, 'username': user.username}
    redis_client.hmset(f"user:{user.id}", user_info)
    redis_client.expire(f"user:{user.id}", 3600)  # Expire after 1 hour
    
    # Get online users from Redis
    online_users = get_online_users(user.id)
    
    emit('login_response', {'user': user_info, 'online_users': online_users})

@socketio.on('send_message')
def handle_message(data):
    sender_id = data.get('sender_id')
    recipient_id = data.get('recipient_id')
    content = data.get('message')
    
    # 保存消息到数据库
    message = Message(
        content=content,
        sender_id=sender_id,
        recipient_id=recipient_id
    )
    db.session.add(message)
    db.session.commit()
    
    # 发送消息给接收者
    emit('new_message', {
        'sender_id': sender_id,
        'content': content,
        'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    }, room=str(recipient_id))

@socketio.on('disconnect')
def handle_disconnect():
    # Remove user from online users in Redis
    for key in redis_client.scan_iter("user:*"):
        user_data = redis_client.hgetall(key)
        if user_data.get(b'username') == request.sid.encode():
            redis_client.delete(key)
            break

def get_online_users(current_user_id):
    online_users = []
    for key in redis_client.scan_iter("user:*"):
        user_data = redis_client.hgetall(key)
        user_id = int(user_data.get(b'id'))
        if user_id != current_user_id:
            online_users.append({
                'id': user_id,
                'username': user_data.get(b'username').decode()
            })
    return online_users

@socketio.on('chat_ai_message')
def handle_chat_ai_message(data):
    user_message = data['message']
    
    # 使用 OpenAI 的 GPT-3 生成 AI 响应
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"User: {user_message}\nAI:",
        max_tokens=150
    )
    
    ai_message = response.choices[0].text.strip()
    
    # 将 AI 的响应发送回客户端
    emit('chat_ai_response', {'message': ai_message})

@socketio.on('get_chat_history')
def handle_get_history(data):
    user1_id = data.get('user1_id')
    user2_id = data.get('user2_id')
    
    # 获取两个用户之间的聊天记录
    messages = Message.query.filter(
        ((Message.sender_id == user1_id) & (Message.recipient_id == user2_id)) |
        ((Message.sender_id == user2_id) & (Message.recipient_id == user1_id))
    ).order_by(Message.timestamp).all()
    
    history = [{
        'sender_id': msg.sender_id,
        'content': msg.content,
        'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for msg in messages]
    
    emit('chat_history', history)

if __name__ == '__main__':
    socketio.run(app, debug=True)

