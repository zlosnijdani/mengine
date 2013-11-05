/**
 * Created with PyCharm.
 * User: abrek
 * Date: 24.10.13
 * Time: 12:50
 * To change this template use File | Settings | File Templates.
 */

var userConnected = function(evt) {
    var id = evt["id"];
    if (user_id == id){
        controlled = new User();
    }
    else{
        var obj = Enemy(id);
        opponents.push(obj);
    }
};

var userMoved = function(evt){
    var id = evt["id"];
    var x = evt["x"];
    var y = evt["y"];
    var player = findPlayer(id, opponents);
    if (player){
        player.x = x;
        player.y = y;
    }
};

function Dispatcher(){
}

Dispatcher.prototype = {
    constructor: Dispatcher,

    do: function(evt) {
        var allowed = {
            "userConnected" : userConnected,
            "userMoved" : userMoved
        };
        var event = $.evalJSON(evt);
        var type_name = event['type'];
        var action = allowed[type_name];
        action(event);
    }

};
