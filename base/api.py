#!/usr/bin/env python                                                                                                                                                                      
#-*- coding: utf-8 -*-

import util


class Responder(object):

    PusherClass = Messages
    ChannelsClass = Channels

    def __init__(self, game_id=None):
        self.room_id = game_id
        self.publisher = Messages().publish

    def to_user(self, user_id, message):
        user_channel = Channels(user_id=user_id).user
        self.publisher(user_channel, message)

    def to_room(self, message):
        room_channel = Channels(room_id=self.room_id).room
        self.publisher(room_channel, message)


class Channels(object):

    app = None
    room_prefix = 'room'
    user_prefix = 'user'
    system_prefix = 'system'

    def __init__(self, room_id=None, user_id=None):
        self.user_id = user_id
        self.room_id = room_id

    def _make_key(*params):
        key = ''.join(map(lambda x: '{0}:'.format(x), params))
        return key[:len(key)-1]

    @property
    def user(self):
        if self.user_id:
            return self._make_key(self.app, self.user_prefix, self.user_id)

    @property
    def room(self):
        if self.room_id:
            return self._make_key(self.app, self.room_prefix, self.room_id)

    @property
    def system(self):
        return self._make_key(self.system_prefix)


class Messages(object):

    api = util.ConfiguredRedis.instance

    def __init__(self):
        self.pipe = self.api()
        self.channel = self.pipe.pubsub()

    def subscribe(self, channel):
        self.channel.subscribe(channel)

    def unsubscribe(self, channel):
        self.channel.usubscribe(channel)

    def listen(self):
        for message in self.channel.listen():
            if message['type'] == 'message':
                yield message['data']

    def publish(self, channel, message):
        self.pipe.publish(channel, message)