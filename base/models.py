#!/usr/bin/env python                                                                                                                                                                      
#-*- coding: utf-8 -*-

import datetime

from mongoengine import *

connect('test')


class User(Document):

    meta = {
        'abstract': True,
        'indexes': ['uid'],
    }

    uid = StringField()
    avatar = StringField()
    money = LongField()
    points = LongField()


class Player(EmbeddedDocument):

    uid = StringField(default='')


class Room(Document):

    meta = {
        'abstract': True
    }

    created = DateTimeField(default=datetime.datetime.utcnow)
    players = MapField(EmbeddedDocument(Player), default=Player)