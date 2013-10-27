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
            'userConnected': self._user_connected,
            'userMoved': self._user_moved,
        }
        self._user = user

    def do(self, event):
        if event:
            event, result = self.registred[event['type']](event)
            messenger = Pusher(self._user)
            messenger.send_to(event)
            if result:
                return result

    def _user_connected(self, event):
        event['id'] = self._user
        return event, None

    def _user_moved(self, event):
        return event, None

