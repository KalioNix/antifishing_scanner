<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ page import="java.sql.*" %>
<%@ page import="javax.servlet.http.HttpSession" %>

<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>로그인 결과</title>
    <script>
        function showAlert(message) {
            alert(message);
            location.href = "login.html";
        }
    </script>
</head>
<body>


<%
String url = "jdbc:mysql://localhost:3306/afs_db?useUnicode=true&serverTimezone=Asia/Seoul";

Connection conn = null;
PreparedStatement pstmt = null;
ResultSet rs = null;

String email = request.getParameter("email");
String password = request.getParameter("password");

Class.forName("com.mysql.jdbc.Driver");

if (email != null && password != null) {
    try{
        conn = DriverManager.getConnection(url, "afs", "1q2w3e4r!");

        String query = "SELECT * FROM users WHERE email = ? AND password = ?";

        pstmt = conn.prepareStatement(query);
        pstmt.setString(1, email);
        pstmt.setString(2, password);
        rs = pstmt.executeQuery();

        if (rs.next()) {
            HttpSession afs_session = request.getSession();
            afs_session.setAttribute("userEmail", email);
            response.sendRedirect("index.html");
        } else {
            out.println("<script>showAlert('로그인에 실패하였습니다.');</script>");
        }

    }catch (Exception e) {
        e.printStackTrace();
    } finally {
        // 리소스 해제
        if (rs != null) rs.close();
        if (pstmt != null) pstmt.close();
        if (conn != null) conn.close();
    }
}

%>
</body>

