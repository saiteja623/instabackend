var words=['hippo','aircraft',
'airline','album','alcohol','alive','all','alliance','rhinosorous','chain','certainly',
'chamber','challenge','champion','championship','chance','change','changing','channel','chapter','character','characteristic','characterize',
'disagree','disappear',
'disaster','discipline','discourse','discover','discovery','discrimination','emergency','emission','emotion','emotional','emphasis','emphasize','employ','employee','employer','employment','empty','enable','encounter','encourage','generally','eneral','generate','generation','gentleman','genetic','instruction','instructor','insurance','instrument','intellectual','intelligence','intend','intense','intensity','intention','interaction'
];
var i=0;
var time=4;
var score=0;
function countdown(){
        var x=document.getElementById('time');
        if (time>=0){
                if(time==4)
                {
                        document.getElementById('msg').innerHTML="";
                }
                x.innerHTML="Time left: " + time;
                time--;
        }
        if(time==-1){
        document.getElementById('msg').innerHTML="Game Over!";
        score=0;
        alert("you lost");
        clearInterval(id);
        }
}
var id=setInterval(countdown,1000);
question();
function question(){
        document.getElementById("word").innerHTML=words[i];
        document.getElementById('input').value="";
}
function scores(){
        score=score+1;
        document.getElementById("score").innerHTML="score: "+ score;
}
function checkWin(){
        var x=document.getElementById('input');
        if (x.value==words[i])
        {
                document.getElementById('msg').innerHTML="correct!!";
                if(i<words.length-1)
                {
                        clearInterval(id);
                        time=4;
                        id=setInterval(countdown,1000);
                        i=Math.floor(Math.random()* words.length);
                        scores();
                        question();
                }
        else{
                alert("game over");
                clearInterval(id);
        }
        }
}
