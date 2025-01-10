from flask import Flask, jsonify, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import requests

app = Flask(__name__)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feijige.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 数据模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# API路由
@app.route('/api/admin/dashboard')
def get_dashboard_data():
    total_users = User.query.count()
    total_projects = Project.query.count()
    active_users = User.query.filter_by(status='active').count()
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()

    return jsonify({
        'totalUsers': total_users,
        'totalProjects': total_projects,
        'activeUsers': active_users,
        'recentUsers': [{
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'status': user.status
        } for user in recent_users]
    })

@app.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

@app.route('/api/admin/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'status' in data:
        user.status = data['status']
    
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@app.route('/login', methods=['POST'])
def login():
    # 获取用户输入的验证码答案
    captcha_response = request.form['captcha']
    if int(captcha_response) != 7:
        return jsonify({"error": "Invalid captcha response"}), 400

    # 处理登录逻辑
    # 如果登录成功
    return redirect('/dashboard')
    # 如果登录失败
    # return jsonify({"error": "Invalid username or password"}), 401

if __name__ == '__main__':
    # 创建数据库表
    with app.app_context():
        db.create_all()
    
    # 启动服务器
    app.run(debug=True) 