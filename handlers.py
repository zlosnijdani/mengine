#!/usr/bin/env python                                                                                                                                                                      
#-*- coding: utf-8 -*-

__author__ = 'zld'

from geventwebsocket import WebSocketError
import bottle
from bottle import request, Bottle, abort, template
from modules.logic import Messenger
from modules import control

bottle.TEMPLATE_PATH.insert(0, 'templates')
app = Bottle()

@app.route('/websocket')
def handle_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')
    user = request.forms.getall('user')
    print "asdfa"

    control.GameChannelsControl.activate_channel(user)
    messenger = Messenger(user)
    while True:
        try:
            message = wsock.receive()
            if message:
                messenger.send_to(message)
            response = messenger.listen()
            if response:
                wsock.send(response)
        except WebSocketError:
            break

@app.route('/main')
def render_template():
    return template('home.tpl')

