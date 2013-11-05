#!/usr/bin/env python                                                                                                                                                                      
#-*- coding: utf-8 -*-


from modules.control import GameChannelsControl as control

ROOM = 'room1'


class Pusher(object):

    channeller = control

    def __init__(self, uid, gid):
        self.room_channel = gid
        self.user_channel = uid

    def _send(self, channel, msg):
        self.channeller.api.rpush(channel, msg)

    def send_to_room(self, msg):
        for c in control.active_channels():
            self._send(c, msg)

    def sent_to_user(self, msg):
        self._send(self.user_channel, msg)


class Listener(object):

    def __init__(self, channels=()):
        if isinstance(channels, tuple):
            self._channels = channels
        else:
            self._channels = [channels]

    def listen(self):
        msgs = []
        for channel in self._channels:
            msgs.append(control.api.lpop(channel))
        return msgs


class EventDispatcher(object):

    def __init__(self, user):

        self.registred = {
            'userConnected': self._user_connected,
            'userMoved': self._user_moved,
        }
        self._user = user

    def _convert(self, d):
        d = {k: v for k, v in d.items()}
        return d

    def do(self, event):
        if event:
            event = self._convert(event)
            event, result = self.registred[event['type']](event)
            messenger = Pusher(self._user, ROOM)
            messenger.send_to_room(event)
            if result:
                return result

    def _user_connected(self, event):
        event['id'] = self._user
        return event, None

    def _user_moved(self, event):
        event['id'] = self._user
        return event, None
