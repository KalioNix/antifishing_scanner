<%@ page import="java.sql.*" %>
<%@ page import="javax.servlet.http.*" %>
<%@ page contentType="text/plain;charset=UTF-8" %>
<%@ page import="javax.servlet.http.HttpSession" %>

<%
// 세션에서 userEmail 가져오기
HttpSession afs_session = request.getSession();
String userEmail = (String) afs_session.getAttribute("userEmail");

// 데이터베이스 연결 정보 설정
String jdbcUrl = "jdbc:mysql://localhost:3306/afs_db?useUnicode=true&serverTimezone=Asia/Seoul";
String dbUser = "afs";
String dbPassword = "1q2w3e4r!";


try {
    Class.forName("com.mysql.cj.jdbc.Driver");
    Connection connection = DriverManager.getConnection(jdbcUrl, dbUser, dbPassword);

    String getUserIdQuery = "SELECT user_id FROM users WHERE email = ?";
    PreparedStatement getUserIdStatement = connection.prepareStatement(getUserIdQuery);
    getUserIdStatement.setString(1, userEmail);

    ResultSet result = getUserIdStatement.executeQuery();
    int userId = 0; // 초기값 설정

    // 결과에서 user_id를 가져옴
    if (result.next()) {
        userId = result.getInt("user_id");
    }

    // 데이터 삽입 쿼리 작성
    String resultValue = request.getParameter("result");
    String insertQuery = "INSERT INTO reports (user_id, report_date, report_text) VALUES (?, CURDATE(), ?)";
    PreparedStatement preparedStatement = connection.prepareStatement(insertQuery);
    preparedStatement.setInt(1, userId);
    preparedStatement.setString(2, resultValue);

    // 데이터 삽입 실행
    int rowsAffected = preparedStatement.executeUpdate();

    // 삽입 성공 여부에 따라 응답 전송
    if (rowsAffected > 0) {
        response.getWriter().write("success");
    } else {
        response.getWriter().write("failure");
    }

    // 연결 및 리소스 해제
    preparedStatement.close();
    getUserIdStatement.close();
    connection.close();

} catch (Exception e) {
    e.printStackTrace();
    response.getWriter().write("error");
}

%>