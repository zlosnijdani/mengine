var game;
var dispatcher;
var messenger = null;

var run = function(){
    game = new Phaser.Game(800, 600, Phaser.AUTO, 'phaser-example', { preload: preload, create: create, update: update });
    dispatcher = new Dispatcher();
    messenger =  new Messenger("ws://192.168.45.3:8000/websocket", dispatcher);
    messenger.connect();
};
