# -*- coding: utf-8 -*-
import logging as log
from dataish.core import wrapper
import validatish
from convertish import converter

log.basicConfig(level=log.DEBUG)


def _get_sub_schema_by_key(schema, key):
    try:
        int(key)
        log.debug('trying to get key %s on %s'%(key, schema))
        log.debug('returning schema.attr, %r'%schema.attr)
        return schema.attr
    except ValueError:
        log.debug('**',key)
        log.debug('returning schema.get(\'%s\'), %r'%(key, schema.get(key)))
        return schema.get(key)


def _wrapif(self, key, value):
    log.debug('schema, key', self.schema, key, value)
    schema = _get_sub_schema_by_key(self.schema, key)
    if isinstance(value, dict):
        log.debug('.. sWrapper(%r), %r'%(value, schema))
        return Wrapper(value, schema)
    if isinstance(value, list):
        log.debug('.. sListWrapper(%r), %s'%(value, schema))
        return ListWrapper(value, schema)
    return value

class Wrapper(wrapper.Wrapper):

    def __init__(self, value, schema):
        self.schema = schema
        wrapper.Wrapper.__init__(self, value)

    def validate(self):
        return self.schema.validate(self)

    def convert(self, _from, _to):
        log.debug('convert from %s to %s'%(_from, _to))
        return converter(_from, _to).convert(self.schema, self)

    def form(self, name=None, action_url=None, errors=None, renderer=None):
        f = form(self, self.schema, defaults=self, errors=None, action_url=None, renderer=None)

    def _wrapif(self, key, value):
        return _wrapif(self, key, value)


class ListWrapper(wrapper.ListWrapper):

    def __init__(self, value, schema):
        self.schema = schema
        wrapper.ListWrapper.__init__(self, value)

    def validate(self):
        return self.schema.validate(self)

    def convert(self, _from, _to):
        log.debug('convert from %s to %s'%(_from, _to))
        return converter(_from, _to).convert(self.schema, self)

    def _wrapif(self, key, value):
        return _wrapif(self, key, value)



