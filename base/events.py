#!/usr/bin/env python                                                                                                                                                                      
#-*- coding: utf-8 -*-

from schematics.models import Model
from schematics.types import base


class BaseEvent(Model):

    type = None
    signature = base.StringType(default=None)


class Authorize(BaseEvent):

    type = 'authorize'

    user_id = base.StringType()
    network = base.StringType()