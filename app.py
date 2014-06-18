#!/usr/bin/env python                                                                                                                                                                      
#-*- coding: utf-8 -*-

import time

from flask import Flask
from flask import request

from base import handlers

app = Flask(__name__)


@app.route('/socket')
def wsocket():

    def on_receive():
        return {'msg': 'hello %s' % int(time.time())}

    def on_send():
        while True:
            yield {'msg': 'ping %s' % int(time.time())}
            time.sleep(2)

    def on_open():
        print "On open actions"

    def on_close():
        print "On close actions"

    handler = handlers.WebSocketHandler(request, request.environ['wsgi.websocket'])
    handler(on_receive, on_send, on_open, on_close)


@app.route('/')
def test():
    return """ <!DOCTYPE html>
<html>
  <head>
    <script type="text/javascript">
       var ws = new WebSocket("ws://localhost:8000/socket");
       ws.onopen = function() {
           //ws.send("socket open");
       };
       ws.onclose = function(evt) {
           alert("socket closed");
       };
    </script>
  </head>
</html> """

app.DEBUG = True
