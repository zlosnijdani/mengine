#!/usr/bin/env python                                                                                                                                                                      
#-*- coding: utf-8 -*-

__author__ = 'zld'

from util import ConfiguredRedis


class GameChannelsControl(object):

    api = ConfiguredRedis.instance()
    active_channels_key = 'mengine:active'

    @classmethod
    def active_channels(cls):
        return cls.api.smembers(cls.active_channels_key)

    @classmethod
    def activate_channel(cls, name):
        cls.api.sadd(cls.active_channels_key, name)

    @classmethod
    def deactivate_channel(cls, name):
        cls.api.sadd(cls.active_channels_key, name)

