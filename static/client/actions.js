var userConnected = function(evt) {
    var id = evt["id"];
    var x = evt['position']['x'];
    var y = evt['position']['y'];

    if (user_id == id){
        controlled = new User(x,y);
    }
    else{
        var obj = new Enemy(id, x,y);
        opponents.push(obj);
    }
};

var userDisconnected = function(evt) {
    var enemy = findPlayer(evt['id'], opponents);
    removePlayer(enemy.id, opponents);
    enemy.sprite.kill()
};

var userMoved = function(evt){
    var id = evt["id"];
    var x = evt["x"];
    var y = evt["y"];
    var player = findPlayer(id, opponents);
    if (player){
        player.sprite.x = x;
        player.sprite.y = y;
    }
};

var State = function(evt){
    var players = evt['players'];

    for (var i=0; i < players.length; i++){
        var id = players[i]['id'];
        var x = players[i]['position']['x'];
        var y = players[i]['position']['y'];
        var enemy = findPlayer(id, opponents);
        if (!enemy){
            opponents.push(new Enemy(id,x,y));
        }
    }
};


function Dispatcher(){
}

Dispatcher.prototype = {
    constructor: Dispatcher,

    do: function(evt) {
        var allowed = {
            "userConnected" : userConnected,
            "userMoved" : userMoved,
            "getState" : State,
            "userDisconnected": userDisconnected
        };
        var event = $.evalJSON(evt);
        var type_name = event['type'];
        var action = allowed[type_name];
        action(event);
    }

};
