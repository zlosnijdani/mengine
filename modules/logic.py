#!/usr/bin/env python                                                                                                                                                                      
#-*- coding: utf-8 -*-

import json
import random
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
        for c in self.channeler.active_channels:
            self._send(c, msg)

    def sent_to_user(self, uid, msg):
        channel = get_channel_name(self.room_channel, uid)
        self._send(channel, msg)


class Listener(object):

    def __init__(self, channel):
        self._channel = channel

    def listen(self):
        while True:
            yield control.api.blpop(self._channel)[1]


class EventsMapping(object):

    owner = 0
    enemies = 1
    all_players = 2

    registred = {
        'userConnected': owner,
        'userMoved': all_players,
        'getState': owner,
        'userDisconnected': enemies,
        'system': owner,
    }



class EventDispatcher(object):

    def __init__(self, user):

        self.registred = {
            'userConnected': self._user_connected,
            'userMoved': self._user_moved,
            'getState': self._get_state,
            'userDisconnected': self._user_disconnected,
            'system': self._system,
        }
        self._user = user

    def do(self, event, view):
        if event:
            return self.registred[event['type']](event, view)

    def _system(self, event, view):
        return event

    def _user_connected(self, event, view):
        p = view.add_player(event['id'])
        x, y = random.randint(0, 400), random.randint(0, 400)
        p.update_position((x, y,))
        event['position'] = {
            'x': x,
            'y': y
        }
        return event

    def _user_disconnected(self, event, view):
        view.remove_player(event['id'])
        return event

    def _user_moved(self, event, view):
        return event

    def _get_state(self, event, view):
        type_name = 'getState'
        players = []
        for player in view.players:
            if player.xid != self._user:
                players.append({'id': player.xid, 'position': {'x': player.x, 'y': player.y}})
        state = {
            'type': type_name,
            'players': players
        }
        return state


class Room(object):

    ViewClass = models.RoomView

    def __init__(self, room_id, uid):
        self.rid = room_id
        self.uid = uid
        self.dispatcher = EventDispatcher(uid)
        self.pusher = Pusher(room_id)
        self.listener = Listener('{0}:{1}'.format(room_id, uid))
        self.to = {EventsMapping.all_players: self._to_all,
                   EventsMapping.enemies: self._to_opponents,
                   EventsMapping.owner: self._to_owner}
        self.view = self.ViewClass.with_id(xid=self.rid)

    @property
    def active_players(self):
        return list(self.view.active)

    @classmethod
    def create_for(cls, room_id, uid):
        if not room_id:
            view = models.RoomView()
            view.save()
            room_id = view.id
        return cls(room_id, uid)

    def _opponents(self):
        players = list(self.view.active)
        players = [player for player in players if player != self.uid]
        return players

    def _to_all(self, event):
        self.pusher.sent_to_room(event)

    def _to_opponents(self, event):
        for enemy in self._opponents():
            self.pusher.sent_to_user(enemy, event)

    def _to_owner(self, event):
        self.pusher.sent_to_user(self.uid, event)

    def user_input(self, event):
        view = self.view
        result = self.dispatcher.do(event, view)
        to = EventsMapping.registred[event['type']]
        self.to[to](json.dumps(result))

    def listen(self):
        return self.listener.listen()