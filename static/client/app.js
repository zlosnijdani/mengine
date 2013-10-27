/**
 * Created with PyCharm.
 * User: abrek
 * Date: 24.10.13
 * Time: 12:49
 * To change this template use File | Settings | File Templates.
 */
var game;
var dispatcher;
var messenger = null;

var run = function(){
    game = new Phaser.Game(800, 600, Phaser.AUTO, 'phaser-example', { preload: preload, create: create, update: update });
    dispatcher = new Dispatcher();
    messenger =  new Messenger("ws://127.0.0.1:8000/websocket", dispatcher);
    messenger.connect();
};
