#!/usr/bin/env python                                                                                                                                                                      
#-*- coding: utf-8 -*-

__author__ = 'zld'
import json
from geventwebsocket import WebSocketError
import bottle
from bottle import request, response, Bottle, abort, template
from modules import logic
from modules import control
import gevent
from bottle import view
from bottle import static_file
from modules.logic import EventDispatcher

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
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')

    user = request.get_cookie("user")
    control.GameChannelsControl.activate_channel(user)
    dispatcher = EventDispatcher(user)
    listener = logic.Listener(user)

    print "user {0} come".format(user)

    while True:
        try:
            message = wsock.receive()
            if message is None:
                break

            if message:
                message = json.loads(message)

            dispatcher.do(message)

            response = listener.listen()

            if response:
                wsock.send(response)

        except:
            print "exception"
            control.GameChannelsControl.deactivate_channel(user)
            raise
    print "deactivate"
    control.GameChannelsControl.deactivate_channel(user)

@app.route('/main')
@view('home.tpl')
def render_template():
    user = request.GET.get('user')
    response.set_header("Set-Cookie", 'user={0}'.format(user))
    print user
    return dict()

@app.route('/static/<filepath:path>')
def handle_static(filepath):
    return static_file(filepath, './static')