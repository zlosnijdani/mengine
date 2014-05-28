#!/usr/bin/env python                                                                                                                                                                      
#-*- coding: utf-8 -*-

import redis

instances = {}


class ConfiguredRedis(object):

    global instances
    api = redis.Redis

    @classmethod
    def instance(cls):
        if not instances:
            instances['redis'] = cls.api(host='localhost', port=6379)
        return instances['redis']
