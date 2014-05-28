#!/usr/bin/env python                                                                                                                                                                      
#-*- coding: utf-8 -*-

__author__ = 'zld'
import gevent
import json
from geventwebsocket import WebSocketError
import bottle
from bottle import request, response, Bottle, abort, template
from modules import logic
from modules import control
from bottle import view
from bottle import static_file
from gevent import monkey

monkey.patch_all()

def log_request(self):
    log = self.server.log
    if log:
        if hasattr(log, "info"):
            log.info(self.format_request() + '\n')
        else:
            log.write(self.format_request() + '\n')

gevent.pywsgi.WSGIHandler.log_request = log_request

bottle.TEMPLATE_PATH.insert(0, 'templates')
app = Bottle()

@app.route('/websocket')
def handle_websocket():
    try:
        wsock = request.environ.get('wsgi.websocket')

        if not wsock:
            abort(400, 'Expected WebSocket request.')

        user = request.get_cookie("user")
        room_id = '529f718c7f42dd3c9af7ba23'
        control_c = control.GameChannelsControl(room_id)

        if room_id:
            control_c.activate_channel(logic.get_channel_name(room_id, user))

        room = logic.Room.create_for(room_id, user)

        def send():

            """
                Send messages to client (Thread 2)
            """

            while True:
                for response in room.listen():
                    if response:
                        json_event = json.dumps(eval(response))
                        wsock.send(json_event)

        while True:
            message = wsock.receive()

            if message is None:
                break
            else:
                message = json.loads(message)
                room.user_input(message)
    except:
        raise

@app.route('/main')
@view('home.tpl')
def render_template():
    user = request.GET.get('user')
    response.set_header("Set-Cookie", 'user={0}'.format(user))
    return dict(user_id=user)

@app.route('/static/<filepath:path>')
def handle_static(filepath):
    return static_file(filepath, './static')