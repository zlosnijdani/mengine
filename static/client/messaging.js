/**
 * Created with PyCharm.
 * User: abrek
 * Date: 24.10.13
 * Time: 12:51
 * To change this template use File | Settings | File Templates.
 */

/*        <script type="text/javascript">
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
*/
function Messenger(url, dispatcher){
    this.dispatcher = dispatcher;
    this.url = url;
}

Messenger.prototype = {
    constructor: Messenger,

    connect : function(){
        this.ws = new WebSocket(this.url);
        var m = this;
        this.ws.onmessage = function(evt){
            m.dispatcher.do(evt.data);
        };
    },
    sendEvent : function(evt){
        this.ws.send($.toJSON(evt));
    }
};

