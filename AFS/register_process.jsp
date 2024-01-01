 <%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="java.sql.*" %>
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>회원가입 결과</title>
    <script>
        function showAlert(message) {
            alert(message);
            location.href = "login.html";
        }
    </script>
</head>
<body>
    <%
        Class.forName("com.mysql.jdbc.Driver");

        String email = request.getParameter("email");
        String username = request.getParameter("username");
        String password = request.getParameter("password");
        String type = request.getParameter("type");

        String url = "jdbc:mysql://localhost:3306/afs_db?useUnicode=true&serverTimezone=Asia/Seoul";

        Connection conn = null;
        PreparedStatement pstmt = null;
        ResultSet rs = null;

        if (email != null && username != null && password != null && type.equals("register")) {
            try{
                conn = DriverManager.getConnection(url, "afs", "1q2w3e4r!");

                String checkEmailSql = "SELECT COUNT(*) FROM users WHERE email=?";
                pstmt = conn.prepareStatement(checkEmailSql);
                pstmt.setString(1, email);
                rs = pstmt.executeQuery();
                rs.next();

                int emailCount = rs.getInt(1);

                if (emailCount > 0) {
                    String errorMessage = "이미 등록된 이메일 주소입니다.";
                    out.println("<script>showAlert('" + errorMessage + "');</script>");
                } else {
                    String insertUserSql = "INSERT INTO users (email, username, password) VALUES (?, ?, ?)";
                    pstmt = conn.prepareStatement(insertUserSql);
                    pstmt.setString(1, email);
                    pstmt.setString(2, username);
                    pstmt.setString(3, password);

                    int rowsAffected = pstmt.executeUpdate();

                    if (rowsAffected > 0) {
                        String successMessage = "회원가입이 완료되었습니다.";
                        out.println("<script>showAlert('" + successMessage + "');</script>");
                    } else {
                        String errorMessage = "회원가입에 실패했습니다.";
                        out.println("<script>showAlert('" + errorMessage + "');</script>");
                    }
                }
            }
            catch(Exception e){
              out.print(e.toString());
            }
            finally {
                if (rs != null) {
                    rs.close();
                }
                if (pstmt != null) {
                    pstmt.close();
                }
                if (conn != null) {
                    conn.close();
                }
            }

        }
    %>
</body>
</html>
