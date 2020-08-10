
function check(){
var x=document.getElementById("valid1");
var y=document.getElementById("valid2");
if(x.value==""||y.value=="")
{
    alert("please fill the information");
    return false;
}
}
function hide(x){
    var y=document.getElementById("valid2")
    x.classList.toggle("fa-eye-slash");
    if(y.type=="password"){
        y.type="text";
    }
    else{
        y.type="password";
    }
}
function logout()
{
    s=confirm("Are u sure u want to Logout");
    return s;
}
function confirmation(otp){
    var x=document.getElementById("otpnum");
    if(x.value!=otp)
    {
        alert("your otp verification failed");
        return false;
    }
}
function menu(){
    setTimeout(load,1000);
}
function load(){
    var x=document.getElementById("loading2");
    x.style.display="none";
    document.getElementById("total").style.display="block";
    }
