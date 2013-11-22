/**
 * Created with PyCharm.
 * User: zld
 * Date: 10/27/13
 * Time: 10:28 PM
 * To change this template use File | Settings | File Templates.
 */


var userMovedEvent = function(uid) {
    var evt = {
        "type": "userMoved",
        "x": 0,
        "y": 0
    };
    evt['id'] = uid;
    return evt
};

var connect = function(uid) {
    var evt = {
        "type": "userConnected"
    };
    evt["id"] = uid;
    return evt
};
