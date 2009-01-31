# -*- coding: utf-8 -*-
import logging as log
from dataish.core import wrapper

log.basicConfig(level=log.INFO)

def _wrapif(self, key, value):
    if isinstance(value, dict):
        log.debug('.. sWrapper(%r)'%value)
        return Wrapper(value, self.schema)
    if isinstance(value, list):
        log.debug('.. sListWrapper(%r), %s'%(value,self.schema))
        return ListWrapper(value, self.schema)
    return value

class Wrapper(wrapper.Wrapper):

    def __init__(self, value, schema):
        self.schema = schema
        wrapper.Wrapper.__init__(self, value)


    def _wrapif(self, key, value):
        return _wrapif(self, key, value)


class ListWrapper(wrapper.ListWrapper):

    def __init__(self, value, schema):
        self.schema = schema
        wrapper.ListWrapper.__init__(self, value)

    def _wrapif(self, key, value):
        return _wrapif(self, key, value)



