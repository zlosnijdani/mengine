#!/usr/bin/env python                                                                                                                                                                      
#-*- coding: utf-8 -*-

__author__ = 'zld'

from util import ConfiguredRedis


class GameChannelsControl(object):

    api = ConfiguredRedis.instance()

    def __init__(self, game_id):
        self.game_id = game_id
        self.key = 'active:%s' % game_id

    @property
    def active_channels(self):
        return self.api.smembers(self.key)

    def activate_channel(self, name):
        self.api.sadd(self.key, name)

    def deactivate_channel(self, name):
        self.api.srem(self.key, name)
        self.clear_channel(name)

    @classmethod
    def clear_channel(cls, name):
        cls.api.delete(name)
