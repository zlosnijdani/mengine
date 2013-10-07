<!DOCTYPE html>
<html>
    <head>
        <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.2.6/jquery.js"> </script>
        <script type="text/javascript">
            function send(ws, message){
                ws.send(message)
            };

            $(document).ready(function(){
            var ws = new WebSocket("ws://127.0.0.1:8000/websocket");
            ws.onopen = function() {
                ws.send("Hello, world");
            };
            ws.onmessage = function (evt) {
                $("#messages").append(evt.data);
            };
                setInterval(send(ws, 'hi'),3000);
            });
        </script>
</head>

    <div id="messages"></div>

</html>