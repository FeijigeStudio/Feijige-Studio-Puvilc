import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;
import java.sql.*;

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
            
            con.close();
        } catch(Exception e) {
            System.out.println(e);
        }
    }
}