<%@ page import="javax.servlet.http.HttpSession" %>
<%
// 현재 세션을 가져옵니다.
HttpSession afs_session = request.getSession();

if (session != null) {
    // 세션을 무효화합니다.
    afs_session.invalidate();
}
response.sendRedirect("index.html"); // 로그아웃 후 이동할 페이지
%>
