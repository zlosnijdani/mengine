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
from modules.logic import EventDispatcher
from gevent.event import AsyncResult
import time
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


class StateWrapper(object):

    """
        Class-wrapper for syncing  two greenlets
    """

    state = False

    @classmethod
    def set_raised(cls):
        cls.state = True

    @classmethod
    def get_state(cls):
        return cls.state

    @classmethod
    def reset(cls):
        cls.state = False


@app.route('/websocket')
def handle_websocket():
    try:
        wsock = request.environ.get('wsgi.websocket')
        if not wsock:
            abort(400, 'Expected WebSocket request.')
        user = request.get_cookie("user")
        room_id = '528e60087f42dd1ed293dc3a'
        control_c = control.GameChannelsControl(room_id)
        if room_id:
            control_c.activate_channel(logic.get_channel_name(room_id, user))
        print room_id
        room = logic.Room.create_for(room_id, user)
        print room
        print "user {0} come".format(user)

        def receive(cstate):

            """
                Receive messages from client (Thread 1)
            """

            while True:
                message = wsock.receive()
                gevent.sleep(0)
                if message is None:
                    print 'stop receiving'
                    print "input %s" % message
                    cstate.set_raised()
                    control_c.deactivate_channel(user)
                    break

                if message:
                    message = json.loads(message)

                room.user_input(message)

        def send(cstate):

            """
                Send messages to client (Thread 2)
            """

            while True:
                if cstate.get_state():
                    print "stop listen"
                    cstate.reset()
                    break
                for response in room.listen():
                    if response:
                        print "output message %s" % response
                        json_event = json.dumps(eval(response))
                        wsock.send(json_event)
                gevent.sleep(0)

        obj = gevent.spawn(receive, StateWrapper)
        obj1 = gevent.spawn(send, StateWrapper)
        gevent.joinall([obj1, obj])
    except:
        raise
@app.route('/main')
@view('home.tpl')
def render_template():
    user = request.GET.get('user')
    response.set_header("Set-Cookie", 'user={0}'.format(user))
    print user
    return dict(user_id=user)

@app.route('/test')
@view('test.tpl')
def render_test():
    return {}

@app.route('/statie/<filepath:path>')
def handle(filepath):
    return static_file(filepath, './static')

@app.route('/static/<filepath:path>')
def handle_static(filepath):
    return static_file(filepath, './static')