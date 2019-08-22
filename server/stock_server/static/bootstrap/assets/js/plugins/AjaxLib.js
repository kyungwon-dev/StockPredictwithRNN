//1. XMLHttpRequest 인스턴스 변수 선언
var xmlHttp;

//2. XMLHttpRequest 인스턴스 변수 셋팅하기 
function createXMLHttpRequest()
{
     if(window.AciveXObject) {
          xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
     } else if (window.XMLHttpRequest) {
          xmlHttp = new XMLHttpRequest();
     } else {
          xmlHttp = new ActiveXObject("Msxml2.XMLHTTP");
     }
}

//3. Request 함수 호출
function startRequest(type, url, fName) {
         createXMLHttpRequest();
         xmlHttp.onreadystatechange = eval(fName);
         xmlHttp.open(type, url, true);
         xmlHttp.send(null);
}
