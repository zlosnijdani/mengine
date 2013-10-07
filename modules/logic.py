#!/usr/bin/env python                                                                                                                                                                      
#-*- coding: utf-8 -*-

__author__ = 'zld'

from modules.control import GameChannelsControl as control


class Messenger(object):

    channeler = control

    def __init__(self, who):
        self.my_channel = who
        self.instance = self.channeler.api
        self.opponent_channel = [channel for channel in self.channeler.active_channels() if channel != who][0]

    def send_to(self, message):
        self.instance.rpush(self.opponent_channel, message)

    def listen(self):
        return self.instance.lpop(self.my_channel)




