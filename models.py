#!/usr/bin/env python                                                                                                                                                                      
#-*- coding: utf-8 -*-
from mongoengine import *

__author__ = 'zld'

connect('main-db')


class GameView(Document):

    meta = {'collection': 'fighter-games'}
    players = ListField()

    @classmethod
    def with_id(cls, xid):
        return cls.objects.get(id=xid)

    def add_player(self, p):
        players = self.players
        if p not in players:
            players.append(p)
            self.players = players
            self.save()

