

function preload() {

    game.load.image('moll', 'static/client/assets/moll.png');
    game.load.image('ventress', 'static/client/assets/ventress.png');

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
            controlled.sprite.y -= 5;
            moved();
        }
        else if (controlled.downKey.isDown)
        {
            controlled.sprite.y += 5;
            moved();
        }

        if (controlled.leftKey.isDown)
        {
            controlled.sprite.x -= 5;
            moved();
        }
        else if (controlled.rightKey.isDown)
        {
            controlled.sprite.x += 5;
            moved();
        }
   }
}
