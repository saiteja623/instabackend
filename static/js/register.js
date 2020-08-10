function check(){
    var x=document.getElementById("name");
    var y=document.getElementById("password1");
    var z=document.getElementById("password2");
    if (x.value==""){
        x.focus();
        x.style.border="2px solid red";
    }
    else{
        x.focus();
        x.style.border="2px solid green";
    }
    if(y.value=="")
    {
        y.focus();
        y.style.border="2px solid red";
    }
    else{
        y.focus();
        y.style.border="2px solid green";
    }
    if(z.value=="")
    {
        z.focus();
        z.style.border="2px solid red";
    }
    if(x.value==""||y.value==""||z.value=="")
    {
        alert("please fill the information");
        return false;
    }
}
function hide1(x){
    var y=document.getElementById("password1")
    x.classList.toggle("fa-eye-slash");
    if(y.type=="password"){
        y.type="text";
    }
    else{
        y.type="password";
    }
}
function hide2(x){
    var y=document.getElementById("password2")
    x.classList.toggle("fa-eye-slash");
    if(y.type=="password"){
        y.type="text";
    }
    else{
        y.type="password";
    }
}
function checkpass(){
    var y=document.getElementById("password1");
    var z=document.getElementById("password2");
    if(y.value!=z.value)
    {
        alert("password didn't match");
        return false;
    }
}