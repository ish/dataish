# -*- coding: utf-8 -*-
import logging as log

log.basicConfig(level=log.DEBUG,)

def _wrapif(self, value):
    if isinstance(value, dict):
        log.debug('.. Wrapper(%r)'%value)
        return Wrapper(value)
    if isinstance(value, list):
        log.debug('.. ListWrapper(%r)'%value)
        return ListWrapper(value)
    return value

class Wrapper(dict):

    def __getattr__(self, key):
        log.debug('__getattr__(%r)'%key)

        try:
            v = self[key]
            log.debug('return self[%r]'%key)
            return v
        except KeyError:
            try:
                v = self.__dict__[key]
                log.debug('return self.__dict__[%r]'%key)
                return v
            except KeyError:
                raise AttributeError()

    def __setattr__(self, key, value):
        log.debug('__setattr__(%r, %r)'%(key, value))
        if key in self:
            log.debug('self[%r] = %r'%(key, value))
            self[key] = value
        else:
            log.debug('self.__dict__[%r] = %r'%(key, value))
            self.__dict__[key] = value


    def __getitem__(self, key):
        item = dict.__getitem__(self, key)
        log.debug('Wrapper.__getitem__(%r)'%key)
        return self._wrapif(item)

    def items(self):
        log.debug('items()')
        return [(key, self[key]) for key in self.keys()]

    def values(self):
        log.debug('values()')
        return [self[key] for key in self.keys()]

    def itervalues(self):
        log.debug('itervalues()')
        return (self[key] for key in self.keys())

    def __repr__(self):
        item = '%r: %r'
        return '❴%s❵'%(', '.join([item%(key, value) for key, value in self.items()]))

    def pop(self, key):
        v = self[key]
        log.debug('pop(%s)'%key)
        del self[key]
        return v

    def popitem(self, key):
        v = self[key]
        log.debug('popitem(%s)'%key)
        del self[key]
        return (key, v)

    def _wrapif(self, value):
        return _wrapif(self, value)


        



class ListWrapper(list):

    def __getitem__(self, key):
        log.debug('ListWrapper.__getitem__(self, %r)'%key)
        item = list.__getitem__(self, key)
        return self._wrapif(item)

    def __iter__(self):
        for item in list.__iter__(self):
            yield self._wrapif(item)

    def __repr__(self):
        return '❲%s❳'%(', '.join('%r'%value for value in self))

    def _wrapif(self, value):
        return _wrapif(self, value)



