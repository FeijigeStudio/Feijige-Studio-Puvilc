from flask import Flask, request, redirect, render_template, session
import mysql.connector
import bcrypt
import re
import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import java.sql.*;
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于session加密

# MySQL连接配置
db_config = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'feijige_community'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # 基本验证
        if not username or not email or not password or not confirm_password:
            return "All fields are required", 400
        if password != confirm_password:
            return "Passwords do not match", 400
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return "Invalid email format", 400

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # 检查用户名是否已存在
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                return "Username already exists", 400

            # 检查邮箱是否已存在
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                return "Email already registered", 400

            # 哈希密码
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # 插入新用户
            query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
            cursor.execute(query, (username, email, hashed_password))
            conn.commit()

            # 注册成功，创建会话
            session['username'] = username
            return redirect('/')

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return "An error occurred during registration", 500

        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True 
            // 执行查询
            ResultSet rs = pstmt.executeQuery();
            
            if (rs.next()) {
                // 登录成功
                HttpSession session = request.getSession();
                session.setAttribute("username", username);
                response.sendRedirect("index.html");
            } else {
                // 登录失败
                response.sendRedirect("login.html?error=1");
            }
            
      public class LoginServlet extends HttpServlet {
    public void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        
        String username = request.getParameter("username");
        String password = request.getParameter("password");
        
        try {
            // 连接到MySQL数据库
            Class.forName("com.mysql.jdbc.Driver");
            Connection con = DriverManager.getConnection(
                "jdbc:mysql://localhost:3306/feijige_community", "username", "password");
            
            // 准备SQL查询
            String sql = "SELECT * FROM users WHERE username = ? AND password = ?";
            PreparedStatement pstmt = con.prepareStatement(sql);
            pstmt.setString(1, username);
            pstmt.setString(2, password);
                con.close();
        } catch(Exception e) {
            System.out.println(e);
        }
    }
})