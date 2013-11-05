<!DOCTYPE html>
<html>
    <head>
        <script type="text/javascript" src="/static/js/jquery-1.10.2.min.js"> </script>
        <script type="text/javascript" src="/static/js/jquery.json-2.4.min.js"> </script>
        <script type="text/javascript" src="/static/js/phaser.js"> </script>
        <script type="text/javascript" src="/static/client/app.js"></script>
        <script type="text/javascript" src="/static/client/events.js"></script>
        <script type="text/javascript" src="/static/client/objects.js"></script>
        <script type="text/javascript" src="/static/js/key.js"> </script>
        <script type="text/javascript" src="/static/client/messaging.js"> </script>
        <script type="text/javascript" src="/static/client/actions.js"> </script>
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
        <button id="join"></button>
        <script type="text/javascript">
            var user_id = "{{ user_id }}";
            $(document).ready(function(){
                run();
                $('#join').click(function(){
                    messenger.sendEvent(connect);
                })
            });
        </script>
   </body>
</html>