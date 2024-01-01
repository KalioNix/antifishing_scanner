<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>AFS</title>
<style>
body {
  margin: 0;
  padding: 0;
  font-family: Arial, Helvetica, sans-serif;
}



#header{
    margin-left: 20em;
    margin-right: 20em;
    margin-bottom: 1.5em;
}

#main_text{
    font-size: 3.0em;
    letter-spacing: 4px;
    font-family: sans-serif;
}
#main_top{
    border-bottom: 2px solid  rgba(29, 76, 120);
    padding-bottom: 1.5em;
}
#main_logo{
    width: 8.0em;
}
.Blue{
    color: rgba(29, 76, 120);
    font-weight: bold;
}

.topnav {
  overflow: hidden;
}

.topnav a {
  float: left;
  color: black;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
  font-size: 20px;
  width: 17%;
}

.topnav a:hover {
  color: rgba(29, 76, 120);
  font-weight: bold;
}

.topnav a.active {
  color: orange;
  font-weight: bold;
}
    
</style>
<script>
window.onload  = function() {
    var path = window.location.pathname;
    var page = path.split("/").pop().split('.')[0]+"_page";
    document.querySelector('.topnav .'+page).className += ' active';
}

</script>
</head>
<body>
    <div id="header">
        <center>
            <div id="main_top">
                <span id="main_text"><span class="Blue">A</span>nti <span class="Blue">F</span>shing <span class="Blue">S</span>canner</span>
                <img src="./hj_images/logo1.png" id="main_logo"/>
            </div>
            <div class="topnav">
                <a class="main_page" href="main.jsp">MAIN</a>
                <a class="news_page" href="news.jsp">NEWS</a>
                <a class="guide_page" href="guide.jsp">GUIDE</a>
                <a class="introduce_page" href="introduce.jsp">INTRODUCE</a>
                <a class="login_page" href="login.jsp">LOGIN</a>
            </div>
        </center>
    </div>
</body>
</html>
