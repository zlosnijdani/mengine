/**
 * Created with PyCharm.
 * User: abrek
 * Date: 24.10.13
 * Time: 12:51
 * To change this template use File | Settings | File Templates.
 */

var controlled = null;
var opponents = [];

function User(){

    this.sprite = game.add.sprite(300, 300, 'me');

    this.upKey = game.input.keyboard.addKey(Phaser.Keyboard.UP);
    this.downKey = game.input.keyboard.addKey(Phaser.Keyboard.DOWN);
    this.leftKey = game.input.keyboard.addKey(Phaser.Keyboard.LEFT);
    this.rightKey = game.input.keyboard.addKey(Phaser.Keyboard.RIGHT);
}

function Enemy(id){
    this.id = id;
    this.sprite = game.add.sprite(100, 300, id);
}

function findPlayer(id, players){
    var match = function(obj){
        if (obj.id === id){
            return obj;
        }
    };

    for (var i=0; i < players.length; i++){
        var result = match(players[i]);
        if (result){
            return result;
        }
    }
}