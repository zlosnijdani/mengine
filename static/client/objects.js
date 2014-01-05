var controlled = null;
var opponents = [];

function User(x,y){

    var s = avatar(user_id);
    this.sprite = game.add.sprite(x, y, s);

    this.upKey = game.input.keyboard.addKey(Phaser.Keyboard.UP);
    this.downKey = game.input.keyboard.addKey(Phaser.Keyboard.DOWN);
    this.leftKey = game.input.keyboard.addKey(Phaser.Keyboard.LEFT);
    this.rightKey = game.input.keyboard.addKey(Phaser.Keyboard.RIGHT);
}

function avatar(id){
    if (id == 'A'){
        return 'moll'
    }
    if (id == 'B'){
        return 'ventress'
    }
}

function Enemy(id, x, y){
    this.id = id;
    var s = avatar(id);
    this.sprite = game.add.sprite(x, y, s);
}

var match = function(id, obj){
    if (obj.id === id){
        return obj;
    }
};

function findPlayer(id, players){

    for (var i=0; i < players.length; i++){
        var result = match(id, players[i]);
        if (result){
            return result;
        }
    }
}

function removePlayer(id, players) {

    var ind = undefined;

    for (var i=0; i < players.length; i++){
        var result = match(id, players[i]);
        if (result){
            ind = i;
            break
        }
    }

    if (ind != undefined) {
        opponents.splice(ind, 1);
    }

}