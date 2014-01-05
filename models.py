#!/usr/bin/env python                                                                                                                                                                      
#-*- coding: utf-8 -*-
from mongoengine import *
__author__ = 'zld'

connect('main-db')


def auto_reload(method):
    def wrapped(self, *args, **kwargs):
        print "asd"
        try:
            self.reload()
        except AttributeError:
            raise
        return method(self, *args, **kwargs)
    return wrapped


def auto_save(method):
    def wrapped(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        self.save()
        return result
    return wrapped


class Player(EmbeddedDocument):

    xid = StringField()
    x = IntField()
    y = IntField()

    def __init__(self, xid, x, y, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)
        self.xid = xid
        self.x = x
        self.y = y

    @property
    def position(self):
        return self.x, self.y

    @auto_save
    def update_position(self, coords):
        self.x, self.y = coords


class RoomView(Document):

    meta = {'collection': 'fighter-games'}
    active_players = ListField()
    players_views = ListField(EmbeddedDocumentField(Player))

    @auto_reload
    @auto_save
    def __init__(self, *args, **kwargs):
        super(RoomView, self).__init__(*args, **kwargs)

    @classmethod
    def with_id(cls, xid):
        return cls.objects.get(id=xid)

    @auto_reload
    @auto_save
    def add_player(self, xid):
        #creates representation
        exist = self.get_player(xid)
        if not exist:
            pinstance = Player(xid, 0, 0)
            self.players_views.append(pinstance)
            pinstance.save = self.save
        else:
            pinstance = exist

        #marks as active
        if xid not in self.active_players:
            self.active_players.append(xid)
        return pinstance

    @auto_save
    def remove_player(self, xid):
        if xid in self.active_players:
            self.active_players.remove(xid)

        players = self.players_views
        ind = None
        for i, p in enumerate(players):
            if xid == p.xid:
                ind = i
        if ind is not None:
            players.pop(ind)
            self.players_views = players

    @property
    @auto_reload
    def players(self):
        return self.players_views

    @property
    @auto_reload
    def active(self):
        return self.active_players

    @auto_reload
    def get_player(self, xid):
        for p in self.players:
            if p.xid == xid:
                #hack for auto updating in "Player" embedded documents
                p.save = self.save
                return p


if __name__ == "__main__":
    v = RoomView()
    v.save()
    v.reload()
