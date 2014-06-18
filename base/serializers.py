#!/usr/bin/env python                                                                                                                                                                      
#-*- coding: utf-8 -*-

import json


class JSONSerializer(object):

    @classmethod
    def loads(cls, msg):
        return json.loads(msg)

    @classmethod
    def dumps(cls, msg):
        return json.dumps(msg)


class XMLSerializer(object):
    pass