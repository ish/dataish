import unittest
from dataish.schema.wrapper import Wrapper
from copy import copy
import schemaish
from validatish import validator as v

import logging as log
import datetime

log.basicConfig(level=log.DEBUG)

def sS(*items):
    return schemaish.Structure(items)
def SI(name, **k):
    return (name, schemaish.Integer(**k))
def SD(name, **k):
    return (name, schemaish.Date(**k))
def SS(name, items):
    return (name, schemaish.Structure(items))
def SQ(name, schema_type):
    return (name, schemaish.Sequence(schema_type))
def sQ(schema_type):
    return schemaish.Sequence(schema_type)

class TestBasic(unittest.TestCase):


    def test_firstchild(self):
        d = {'a': 1, 'b': 2, 'c': datetime.date(1966,1,1)}
        schema = sS(SI('a'),SI('b'),SD('c'))
        w = Wrapper(d, schema)
        out = w.convert('python','json')
        expected = {'a': 1, 'b': 2, 'c': {'month': 1, '__type__': 'date', 'day': 1, 'year': 1966}}
        assert out == expected

    def test_subchildren(self):
        d = {'a': 1, 'b': {'p':12,'q':13}, 'c': {'x':25,'y': datetime.date(1966,1,1)}}
        schema = sS(SI('a'),SS('b',[SI('p'),SI('q')]),SS('c',[SI('x'),SD('y')]))
        w = Wrapper(d, schema)        
        wc = w.c
        out = w.c.convert('python','json')
        expected = {'x':25,'y': {'month': 1, '__type__': 'date', 'day': 1, 'year': 1966}}
        assert out == expected
        out = w.convert('python','json')
        expected = {'a': 1, 'b': {'p':12,'q':13}, 'c': expected}
        assert out == expected


    def test_sublists(self):
        d = {'a': 1, 'b': {'p':12,'q':13}, 'c': [
            {'x':25,'y': datetime.date(1999,12,30)},
            {'x':None,'y': datetime.date(1966,1,1)}]}
        schema = sS(SI('a'),SS('b',[SI('p'),SI('q')]),SQ('c',sS(SI('x'),SD('y'))))
        w = Wrapper(d, schema)
        wc = w.c
        out = wc.convert('python','json')
        expected = [
            {'y': {'month': 12, '__type__': 'date', 'day': 30, 'year': 1999}, 'x': 25}, 
            {'y': {'month': 1, '__type__': 'date', 'day': 1, 'year': 1966}, 'x': None}]
        assert out == expected
        out = w.convert('python','json')
        expected = {'a': 1, 'b': {'p': 12, 'q': 13}, 'c': expected}
        assert out == expected


    def test_sublistnodata(self):
        d = {'a': 1, 'b': {'p':12,'q':13}, 'c': []}
        schema = sS(SI('a'),SS('b',[SI('p'),SI('q')]),SQ('c',sS(SI('x'),SD('y'))))
        w = Wrapper(d, schema)
        wc = w.c
        out = wc.convert('python','json')
        expected = []
        assert out == expected
        out = w.convert('python','json')
        expected = {'a': 1, 'b': {'p': 12, 'q': 13}, 'c': expected}
        assert out == expected



