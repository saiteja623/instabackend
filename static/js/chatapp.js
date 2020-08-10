function loaded(){
    var socket =new WebSocket('ws://127.0.0.1:8000/chat/');
    socket.onopen=socket_open;
    socket.onmessage=socket_message;
    document.getElementById("form").onsubmit(function(e){
            e.preventDefault();
            message_data={
                'username':document.getElementById("input").value,
                'message':document.getElementById("msg").value
            }
            socket.send(JSON.stringify(message_data));
            document.getElementById("form").reset();
    });
};
function socket_open(){
    alert("websocket is open");
}
function socket_message(){
    alert("message recieved");
}