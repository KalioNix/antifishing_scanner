<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>AFS</title>
<style>
body{
    margin:0;
    padding:0;
}


.progress{
  margin-top: 40px;
  font-size: 3em;
}

.barOverflow{ /* Wraps the rotating .bar */
  width: 400px; height: 200px; /* Half circle (overflow) */
  margin-bottom: -14px; /* bring the numbers up */
  overflow: hidden;
}
.bar{
  top: 0; left: 0;
  width: 400px; height: 400px; /* full circle! */
  border-radius: 50%;
  box-sizing: border-box;
  border: 50px solid #ccc;     /* half gray, */
  border-bottom-color: green;  /* half azure */
  border-right-color: green;
}

input[type=text] {
    margin-top: 150px;
  font-size: 25px;
  border: solid 1px black;
  width: 700px;
  height: 40px;
}


button{
    display: inline-block;
    font-size: 30px;
    background: orange;
    color: white;
    width: 140px;
    height: 50px;
    border: none;

}

button:hover{
    width: 143px;
    height: 53px;
    font-weight: bold;
}


.result{
    display: none;
}


</style>

<script src="jquery.js"></script>
<script>
$(document).ready(function(){
$(".progress").each(function(){
  var $bar = $(this).find(".bar");
  var $val = $(this).find("span");
  var perc = parseInt( $val.text(), 10);
 
  $({p:0}).animate({p:perc}, {
    duration: 3000,
    easing: "swing",
    step: function(p) {
      $bar.css({
        transform: "rotate("+ (45+(p*1.8)) +"deg)", // 100%=180° so: ° = % * 1.8
        // 45 is to add the needed rotation to have the green borders at the bottom
      });
      $val.text(p|0);
    }
  });
}); 
});
</script>
</head>

<body>
    <%@ include file="./header.jsp" %>
<%
String url = request.getParameter("url");
String score = request.getParameter("score");

%>
    <center>

        <div class="form">
        <div class="search-container">
            <input type="text" placeholder="https://example.com" name="search">
            <button class="check">CHECK</button>
        </div>
        </div>



        <div>
        <div class="chart">
            <div class="progress">
                <div class="barOverflow">
                    <div class="bar"></div>
                </div>
                <div><span class="score"><%=score%></span>/100</div>
            </div>
        </div>
        </div>

    <div class="result">
        <img src="./hj_images/4.png" class="smile"/>
        </br>

        <button>SCAN</button>
    </div>


    </center>
</body>
</html>
