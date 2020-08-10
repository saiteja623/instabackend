var names=questions();
let  lives=5;
var x=document.querySelectorAll("button");
for(var i=0;i<x.length;i++){
        x[i].addEventListener('click',color);
}
function load(){
        document.getElementById("loading2").style.display="none";
}
function color(){
        
        var y=this.innerHTML;
        var index=checkLetter(y);
                var button =document.getElementsByClassName("randomque");
                if(index.length==0){
                    var x=document.getElementsByClassName("fas fa-heart");
                    x[lives-1].className="far fa-heart";
                    lives-=1;
                    this.style.color="red";
                }
                else{
                for(var i=0;i<index.length;i++){
                        var pos=index[i];
                button[pos].textContent=y;
                this.style.color="green";
                }
            }
                checkWin();
}
function questions(){
        const namesList=["pencil",'eraser','tablets','tamarind','tailor','tall','umbrella','unfair','unfit','chocolate','mother','silver','broken','potato','breath','secret','circle','energy','again','agree','begin','beach','shadow','pillow','tiger'];
        const names=namesList[Math.floor(Math.random() * namesList.length)];
        for(var i=0;i<names.length;i++){
                var div=document.createElement("div");
                div.setAttribute("class","randomque");
        document.getElementById("question").appendChild(div);
}
var button=document.getElementsByClassName("randomque");
button[0].textContent=names[0];
return names;
}
function checkLetter(letter){
        var letters=[];
        for (var i=0;i<names.length;i++){
                if(names[i]===letter){
                        letters.push(i);
                }

        }return letters;
}
function checkWin(){
        var x=document.getElementById('question').textContent;
        if (x==names){
                alert("you have won the game");
                location.reload();
        }
        if(lives==0){
            alert("you have lost the game");
            var button =document.getElementsByClassName("randomque");
            for(var i=0;i<names.length;i++){
                    button[i].textContent=names[i];
            }
            setTimeout(function(){location.reload();},1000);
        }
}
