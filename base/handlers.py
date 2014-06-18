#!/usr/bin/env python                                                                                                                                                                      
#-*- coding: utf-8 -*-

import gevent

from base.serializers import JSONSerializer


class WebSocketHandler(object):

    serializer = JSONSerializer

    def __init__(self, req, ws):
        self.req = req
        self.ws = ws

    def close(self):
        self.ws.close()

    def loads(self, msg):
        return self.serializer.loads(msg)

    def dumps(self, msg):
        return self.serializer.dumps(msg)

    def send(self, msg):

        """
            write serealized message to sock
        """
        self.ws.send(self.dumps(msg))

    def receive(self):

        """
            return deserealized message from client
        """
        return self.loads(self.ws.receive())

    def _handle_send(self, handler):

        """
            expects that handler is generator function
        """
        print handler

        for msg in handler():
            self.send(msg)

    def _handle_receive(self, handler):

        """
            receives messages, until client not disconnect
        """

        while True:
            print "ITERATION"
            in_msg = self.receive()

            print in_msg
            if in_msg is not None:
                answer = handler(in_msg)

                if answer is not None:
                    self.send(answer)
            else:
                break

    def __call__(self, on_msg, on_send, on_open, on_close):

        """
            Start serving
        """

        answer = on_open()

        if answer is not None:
            self.send(answer)

        send_srv = gevent.spawn(self._handle_send, on_send)

        try:
            self._handle_receive(on_msg)
        finally:
            on_close()
            send_srv.kill()
            self.close()
