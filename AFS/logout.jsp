<%@ page import="javax.servlet.http.HttpSession" %>
<%
// ���� ������ �����ɴϴ�.
HttpSession afs_session = request.getSession();

if (session != null) {
    // ������ ��ȿȭ�մϴ�.
    afs_session.invalidate();
}
response.sendRedirect("index.html"); // �α׾ƿ� �� �̵��� ������
%>
