#!/usr/bin/env python                                                                                                                                                                      
#-*- coding: utf-8 -*-

import json
import random
import hashlib
import datetime
import models
from modules.control import GameChannelsControl as control


def get_channel_name(gid, uid):
    return "{0}:{1}".format(gid, uid)


class Pusher(object):

    def __init__(self, gid):
        self.room_channel = gid
        self.channeler = control(gid)

    def _send(self, channel, msg):
        self.channeler.api.rpush(channel, msg)

    def sent_to_room(self, msg):
        print self.channeler.active_channels
        for c in self.channeler.active_channels:
            self._send(c, msg)

    def sent_to_user(self, uid, msg):
        channel = get_channel_name(self.room_channel, uid)
        self._send(channel, msg)


class Listener(object):

    def __init__(self, channels=()):
        if isinstance(channels, tuple):
            self._channels = channels
        else:
            self._channels = (channels,)

    def listen(self):
        msgs = []
        for channel in self._channels:
            msgs.append(control.api.lpop(channel))
        return msgs


class PGroups(object):

    owner = 0
    enemies = 1
    all_players = 2


class EventDispatcher(object):

    def __init__(self, user):

        self.registred = {
            'userConnected': self._user_connected,
            'userMoved': self._user_moved,
        }
        self._user = user

    def do(self, event, view):
        if event:
            return self.registred[event['type']](event, view)

    def _user_connected(self, event, view):
        view.add_player(event['id'])
        return PGroups.all_players, event

    def _user_moved(self, event, view):
        return PGroups.enemies, event


class Room(object):

    ViewClass = models.GameView

    def __init__(self, room_id, uid):
        self.rid = room_id
        self.uid = uid
        self.dispatcher = EventDispatcher(uid)
        self.pusher = Pusher(room_id)
        self.listener = Listener((uid, '{0}:{1}'.format(room_id, uid)))
        self.to = {PGroups.all_players: self._to_all,
                   PGroups.enemies: self._to_opponents,
                   PGroups.owner: self._to_owner}
        self.view = self.ViewClass.with_id(xid=self.rid)

    @classmethod
    def create_for(cls, room_id, uid):
        if not room_id:
            view = models.GameView()
            view.save()
            room_id = view.id
        return cls(room_id, uid)

    def _opponents(self):
        players = list(self.view.players)
        return players

    def _to_all(self, event):
        self.pusher.sent_to_room(event)

    def _to_opponents(self, event):
        print "enemies %s " % self._opponents()
        for enemy in self._opponents():
            print enemy
            self.pusher.sent_to_user(enemy, event)

    def _to_owner(self, event):
        self.pusher.sent_to_user(self.uid, event)

    def user_input(self, event):
        view = self.view
        to, result = self.dispatcher.do(event, view)
        self.to[to](json.dumps(result))

    def listen(self):
        return self.listener.listen()