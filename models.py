#!/usr/bin/env python                                                                                                                                                                      
#-*- coding: utf-8 -*-
from mongoengine import *
__author__ = 'zld'

connect('main-db')


class Player(EmbeddedDocument):

    xid = StringField()
    x = IntField()
    y = IntField()

#    def __init__(self, xid, x, y, *args, **kwargs):
#        super(Player, self).__init__(*args, **kwargs)
#        self.xid = xid
#        self.x = x
#        self.y = y

#    @property
#    def position(self):
#        return self.x, self.y

#    def update_position(self, coords):
#        self.x, self.y = coords


class RoomView(Document):

    meta = {'collection': 'fighter-games'}
    active_players = ListField()
    players_views = ListField(EmbeddedDocumentField(Player))

    def __init__(self, *args, **kwargs):
        super(RoomView, self).__init__(*args, **kwargs)

    @classmethod
    def with_id(cls, xid):
        return cls.objects.get(id=xid)

#    def add_player(self, xid):
        #creates representation
#        exist = self.get_player(xid)
#        if not exist:
#            pinstance = Player(xid, 0, 0)
#            self.players_views.append(pinstance)
#            pinstance.save = self.save
#        else:
#            pinstance = exist

        #marks as active
#        if xid not in self.active_players:
#            self.active_players.append(xid)
#        return pinstance

#    def remove_player(self, xid):
#        if xid in self.active_players:
#            self.active_players.remove(xid)

#        players = self.players_views
#        ind = None
#        for i, p in enumerate(players):
#            if xid == p.xid:
#                ind = i
#        if ind is not None:
#            players.pop(ind)
#            self.players_views = players

#    @property
#    def players(self):
#       return self.players_views

#    @property
#    def active(self):
#        return self.active_players

#    def get_player(self, xid):
#        for p in self.players:
#            if p.xid == xid:
                #hack for auto updating in "Player" embedded documents
#                p.save = self.save
#                return p


#if __name__ == "__main__":
#    v = RoomView()
#    v.save()
#    v.reload()
