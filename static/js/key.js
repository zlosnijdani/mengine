

function preload() {

    game.load.image('phaser', 'static/client/assets/phaser-dude.png');

}


function create() {
    game.stage.backgroundColor = '#736357';
}

function update() {

    var moved = function(){
        var evt = userMovedEvent(user_id);
        evt['x'] = controlled.sprite.x;
        evt['y'] = controlled.sprite.y;
        messenger.sendEvent(evt);
    };

    if (controlled !== null && messenger !== null ){

        if (controlled.upKey.isDown)
        {
            controlled.sprite.y--;
            moved();
        }
        else if (controlled.downKey.isDown)
        {
            controlled.sprite.y++;
            moved();
        }

        if (controlled.leftKey.isDown)
        {
            controlled.sprite.x--;
            moved();
        }
        else if (controlled.rightKey.isDown)
        {
            controlled.sprite.x++;
            moved();
        }
   }
}
