#!/usr/bin/env python                                                                                                                                                                      
#-*- coding: utf-8 -*-

__author__ = 'zld'

from modules.control import GameChannelsControl as control


class Messenger(object):

    channeler = control

    def __init__(self, who):
        self.user = who
        self.my_channel = who

    def send_to(self, message):
        print "ACTIVE_CHANNELS {0}".format(self.channeler.active_channels())
        print "MYCHANNEL {0}".format(self.my_channel)
        opponents_channels = [channel for channel in self.channeler.active_channels() if channel != self.my_channel]
        print "OPPONENT C>HANNELS {0}".format(opponents_channels)
        if opponents_channels:
            [self.channeler.api.rpush(channel, message) for channel in opponents_channels]
            return True
        return False

    def listen(self):
        return self.channeler.api.lpop(self.my_channel)


class EventDispatcher(object):

    def __init__(self, user):

        self.registred = {
            'message': self._on_message,
            '_close': self._close,
        }
        self._user = user

    def do(self, event):
        action = self.registred[event['type']]
        return action(event)

    def _init(self, event):
        user = event['session_id']
        return {'type': 'init', 'user': user}

    def _on_message(self, event):
        messenger = Messenger(self._user)
        messenger.send_to(event['message'])

    def _close(self, event):
        return