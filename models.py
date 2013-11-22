#!/usr/bin/env python                                                                                                                                                                      
#-*- coding: utf-8 -*-
from mongoengine import *

__author__ = 'zld'

connect('main-db')


class doc(Document):

    meta = {'collection': 'fighter-games'}
    players = ListField()


class GameView(object):

    def __init__(self, xid):
        self._doc = doc.objects(id=xid)

    def add_player(self, player):
        print "players before {0}".format(self._doc.players)
        if player not in self._doc.players:
            #self.__class__.objects(id=self.id).update(push__players=player)
            p = list(self._doc.players())
            print p
            p.append(player)
            self._doc.players = p
            self._doc.save()
        print "players after {0}".format(self._doc.players)


def clear():
    #v = GameView('528e60087f42dd1ed293dc3a')
    #v.add_player('b')
    print doc.objects.get(id='528e60087f42dd1ed293dc3a')
#        c =  d.players
#        c.append('a')
#        d.players= c
#        print d.players



if __name__ == '__main__':
    clear()

