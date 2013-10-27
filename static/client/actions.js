/**
 * Created with PyCharm.
 * User: abrek
 * Date: 24.10.13
 * Time: 12:50
 * To change this template use File | Settings | File Templates.
 */

function Dispatcher(){
    this.allowed = {
        'user_connected' : this.user_connected
    }
}

Dispatcher.prototype = {
    constructor: Dispatcher,

    do: function(evt) {
        var event = $.evalJSON($.quoteString(evt));
        var type_name = event['type'];
        var action = this.allowed[type_name];
        action(evt);
    },
    userConnected: function(evt) {
        var id = evt['id'];
        var obj = Enemy(id);
        opponents.push(obj);
    },

    userMoved: function(evt){
        var id = evt['id'];
        var x = evt['x'];
        var y = evt['y'];
        var player = findPlayer(id, opponents);
        if (player){
            player.x = x;
            player.y = y;
        }
    }
};



