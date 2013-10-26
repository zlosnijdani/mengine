<!DOCTYPE html>
<html>
    <head>
        <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.2.6/jquery.js"> </script>
        <script type="text/javascript" src="/static/js/jquery.json-2.4.min.js"> </script>
        <script type="text/javascript" src="/static/client/app.js"></script>
        <script type="text/javascript" src="/static/client/dispatcher.js"></script>
        <script type="text/javascript" src="/static/client/app.js"> </script>
        <script type="text/javascript" src="/static/client/draw.js"> </script>
<!--        <script type="text/javascript">
            $(document).ready(function(){
                var ws = new WebSocket("ws://127.0.0.1:8000/websocket");
              //  ws.onopen = function() {
              //  };
                ws.onmessage = function (evt) {
                    $("#messages").append(evt.data);
                };

                setInterval(function(){
                    var wrapper = {"type":"message"};
                    wrapper["message"] = "hello";
                    ws.send($.toJSON(wrapper))
                },3000);


            });
            app();
        </script>
-->
        <style>
            #GameScene {
                margin: 10% auto;
                width: 760px;
                height: 1000px;
            }

            #GameField {
                width: 760px;
                height: 600px;
                border:1px solid #000000;
                background-color: lightgrey;
                display: block;
            }
        </style>

   </head>
   <body>
        <div id="GameScene">
            <canvas id="GameField"></canvas>
        </div>
   </body>
</html>