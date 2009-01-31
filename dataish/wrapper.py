import logging as log

log.basicConfig(level=log.DEBUG,)

def reduce_keylevel(d):
    for k, v in d:
        segments = k.split('.')
        d['.'.join(segments[1:])] = v
    return d
        

class Wrapper(object):

    def __init__(self, dict, wrap_children=True, class_register=None,**k):
        self.__subject__ = dict
        if class_register is None:
            self.__class_register__ = {}
        else:
            self.__class_register__ = class_register
        self.__wrap_children__ = wrap_children
        self.foo = 'foo'


    def __getattr__(self, name):
        log.debug('__getattr__(self, %r)'%name)
        if name == '__subject__':
            log.debug('return self.__dict__[\'__subject__\']')
            return self.__dict__['__subject__']
        if name in self.__subject__:
            log.debug('getting dict value via  getattr')
            if self.__wrap_children__ == True and isinstance(self.__subject__[name], dict):
                log.debug('..wrapping child')
                out = Wrapper(self.__subject__[name], wrap_children=self.__wrap_children__, class_register=reduce_keylevel((self.__class_register__)))
            else:
                log.debug('..not wrapping child')
                out = self.__subject__[name]
            log.debug('..looking up on the class register')
            log.debug('self.__clas__register__ %s'%self.__class_register__, name)
            func = self.__class_register__.get(name,lambda x: x)
            return func(out)            
        if name in self.__dict__:
            log.debug('getting value via class dict')
            return self.__dict__[name]

        raise AttributeError()

    def __setattr__(self, name, value):
        log.debug('__setattr__(self, %r, %r)'%(name, value))
        if name == '__subject__':
            log.debug('setting the subject')
            self.__dict__['__subject__'] = value
            return
        if name in self.__subject__:
            log.debug('setting an entry on the subject dict')
            self.__dict__['__subject__'][name] = value
            return
        log.debug('setting value via setattr')
        self.__dict__[name] = value


