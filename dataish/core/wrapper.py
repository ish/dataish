# -*- coding: utf-8 -*-
import logging as log

log.basicConfig(level=log.INFO)

def _wrapif(self, key, value):
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
        log.debug('__setattr__(%s, %r)'%(key, value))
        if key in self:
            log.debug('self[%r] = %r'%(key, value))
            self[key] = value
        else:
            log.debug('self.__dict__[%r] = %r'%(key, value))
            self.__dict__[key] = value


    def __getitem__(self, key):
        value = dict.__getitem__(self, key)
        log.debug('Wrapper.__getitem__(%r)'%key)
        
        return self._wrapif(key, value)

    def items(self):
        log.debug('items()')
        return [(key, self[key]) for key in self.keys()]

    def values(self):
        log.debug('values()')
        return [self[key] for key in self.keys()]

    def itervalues(self):
        log.debug('itervalues()')
        return (self[key] for key in self.keys())

    def iteritems(self):
        log.debug('iteritems()')
        return ((key, self[key]) for key in self.keys())

    def __repr__(self):
        item = '%r: %r'
        return '❴%s❵'%(', '.join([item%(key, value) for key, value in self.items()]))

    def pop(self, key):
        value = dict.pop(self, key)
        log.debug('pop(%s)'%key)
        return self._wrapif(key, value)

    def get(self, key):
        value = dict.get(self,key)
        log.debug('get(%s)'%key)
        return self._wrapif(key, value)

    def popitem(self, key):
        v = self.pop(key)
        log.debug('popitem(%s)'%key)
        return (key, v)

    def _wrapif(self, key, value):
        return _wrapif(self, key, value)


        



class ListWrapper(list):

    def __getitem__(self, key):
        log.debug('ListWrapper.__getitem__(self, %r)'%key)
        item = list.__getitem__(self, key)
        return self._wrapif(key, item)

    def __iter__(self):
        for n, item in enumerate(list.__iter__(self)):
            log.debug('__iter__()',n,item)
            yield self._wrapif(n, item)

    def __repr__(self):
        return '❲%s❳'%(', '.join('%r'%value for value in self))

    def _wrapif(self, key, value):
        return _wrapif(self, key, value)



