#!/usr/bin/env python                                                                                                                                                                      
#-*- coding: utf-8 -*-

__author__ = 'zld'

from modules.control import GameChannelsControl as control


class Pusher(object):

    channeler = control

    def __init__(self, who):
        self.user = who
        self.my_channel = who

    def send_to(self, message):
        opponents_channels = [channel for channel in self.channeler.active_channels() if channel != self.my_channel]
        if opponents_channels:
            [self.channeler.api.rpush(channel, message) for channel in opponents_channels]
            return True
        return False


class Listener(object):

    def __init__(self, who):
        self.my_channel = who

    def listen(self):
        return control.api.lpop(self.my_channel)


class EventDispatcher(object):

    def __init__(self, user):

        self.registred = {
            'message': self._on_message,
            '_close': self._close,
        }
        self._user = user

    def do(self, event):
        if event:
            print "event %s" % event
            action = self.registred[event['type']]
            return action(event)

    def _init(self, event):
        user = event['session_id']
        return {'type': 'init', 'user': user}

    def _on_message(self, event):
        messenger = Pusher(self._user)
        messenger.send_to(event['message'])

    def _close(self, event):
        return