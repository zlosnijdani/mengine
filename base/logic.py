#!/usr/bin/env python
#-*- coding: utf-8 -*-


class RegisterEventsMeta(type):
    """
        Saves events and bound handlers to class object
    """
    def __new__(mcs, name, bases, attrs):
        new_class = super(RegisterEventsMeta, mcs).__new__(mcs, name, bases, attrs)
        new_class.mapping = dict()
        new_class.events = dict()

        for value in attrs.itervalues():
            if hasattr(value, 'event'):
                method = value
                new_class.mapping[method.event.type] = method
                new_class.events[method.event.type] = method.event

        return new_class


def on_event(event_class):
    """
    Binds event class to handler

    Usage example:

        @on_event(MyEventClass)
        def func(self, params)
            ...

    """
    def wrapper(func):
        func.event = event_class
        return func
    return wrapper


class UnknownEvent(Exception):
    pass


class EventDispatcher(object):

    __metaclass__ = RegisterEventsMeta

    def _find_ev_cls(self, type_name):
        try:
            return self.events[type_name]
        except KeyError:
            raise UnknownEvent("Try to call unregistered event {0}".format(type_name))

    def _fill_ev_obj(self, event_class, raw):
        del raw['type']
        return event_class(raw)

    def __call__(self, raw):
        cls = self._find_ev_cls(raw['type'])
        obj = self._fill_ev_obj(cls, raw)
        return self.mapping[cls.type](self, obj)