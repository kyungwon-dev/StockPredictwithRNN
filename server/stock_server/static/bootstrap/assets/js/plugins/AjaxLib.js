//1. XMLHttpRequest �ν��Ͻ� ���� ����
var xmlHttp;

//2. XMLHttpRequest �ν��Ͻ� ���� �����ϱ� 
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

//3. Request �Լ� ȣ��
function startRequest(type, url, fName) {
         createXMLHttpRequest();
         xmlHttp.onreadystatechange = eval(fName);
         xmlHttp.open(type, url, true);
         xmlHttp.send(null);
}
