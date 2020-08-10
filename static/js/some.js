var ob;
var csrfcookie = function() {
    var cookieValue = null,
        name = 'csrftoken';
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};
function clicked(){
    var x=document.getElementById("input").value;
    const params='val='+x+ '&val2=something';
ob=new XMLHttpRequest();
ob.open("POST","number",true);
ob.setRequestHeader('Content-type','application/x-www-form-urlencoded');
ob.setRequestHeader('X-CSRFToken', csrfcookie());
ob.onreadystatechange=callback;
ob.send(params);
}   
function callback(){
    console.log(ob.readyState);
    console.log(ob.status);
    if(ob.readyState==4){
        document.getElementById("random").innerHTML=ob.responseText;
    };
};