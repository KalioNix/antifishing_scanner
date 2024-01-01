<%@ page import="java.sql.*" %>
<%@ page import="javax.servlet.http.*" %>
<%@ page contentType="text/plain;charset=UTF-8" %>
<%@ page import="javax.servlet.http.HttpSession" %>

<%
// 세션에서 userEmail 가져오기
HttpSession afs_session = request.getSession();
int report_id = Integer.parseInt(request.getParameter("report_id"));
String report_text = (String) afs_session.getAttribute("report_text");


// 데이터베이스 연결 정보 설정
String jdbcUrl = "jdbc:mysql://localhost:3306/afs_db?useUnicode=true&serverTimezone=Asia/Seoul";
String dbUser = "afs";
String dbPassword = "1q2w3e4r!";

try {
    Class.forName("com.mysql.cj.jdbc.Driver");
    Connection connection = DriverManager.getConnection(jdbcUrl, dbUser, dbPassword);

    // 데이터 삽입 쿼리 작성
    String resultValue = request.getParameter("result");
    String insertQuery = "delete from reports where report_id = ?";
    PreparedStatement preparedStatement = connection.prepareStatement(insertQuery);
    preparedStatement.setInt(1, report_id);

    // 데이터 삭제 실행
    int rowsAffected = preparedStatement.executeUpdate();

    // 삽입 성공 여부에 따라 응답 전송
    if (rowsAffected > 0) {
        response.getWriter().write("success");
    } else {
        response.getWriter().write("failure");
    }

    // 연결 및 리소스 해제
    preparedStatement.close();
    connection.close();

} catch (Exception e) {
    e.printStackTrace();
    response.getWriter().write("error");
}

%>