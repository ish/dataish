import unittest
from dataish.schema.wrapper import Wrapper
from copy import copy
import schemaish

import logging as log

log.basicConfig(level=log.INFO)

def sS(*items):
    return schemaish.Structure(items)
def SI(name):
    return (name, schemaish.Integer())
def SS(name, items):
    return (name, schemaish.Structure(items))
def SQ(name, schema_type):
    return (name, schemaish.Sequence(schema_type))
def sQ(schema_type):
    return schemaish.Sequence(schema_type)

def setUp(self):
    self.d1 = {'a': 1, 'b': 2, 'c': 3}
    self.schema1 = sS(SI('a'),SI('b'),SI('c'))
    self.simpledict = Wrapper(self.d1, self.schema1)

    self.d2 = {'a': 1, 'b': {'p':12,'q':13}, 'c': {'x':25,'y': 26}}
    self.schema2 = sS(SI('a'),SS('b',[SI('p'),SI('q')]),SS('c',[SI('x'),SI('y')]))
    self.nesteddict = Wrapper(self.d2, self.schema2)

    self.d3 = {'a': 1, 'b': {'p':12,'q':13}, 'c': [{'x':25,'y': 26},]}
    self.schema3 = sS(SI('a'),SS('b',[SI('p'),SI('q')]),SQ('c',sS(SI('x'),SI('y'))))
    self.nesteddict_withseq = Wrapper(self.d3, self.schema3)

    self.d4 = {'a': 1, 'b': {'p':12,'q':13}, 'c': [[{'x':25,'y': 26},],]}
    self.schema4 = sS(SI('a'),SS('b',[SI('p'),SI('q')]),SQ('c',sQ(sS(SI('x'),SI('y')))))
    self.nesteddict_withnestedseq = Wrapper(self.d4, self.schema4)

class TestBasic(unittest.TestCase):

    def setUp(self):
       setUp(self) 


    def test_firstchild(self):
        w = self.simpledict
        assert w.a == w['a']
        assert w.b == w['b']
        assert w.c == w['c']
        assert w.schema == self.schema1

    def test_subchildren(self):
        w = self.nesteddict
        assert w.c == w['c']
        assert w.c.x == w['c']['x']
        assert w.c.y == w['c']['y']
        assert w.c.schema == self.schema2.get('c')

    def test_sublists(self):
        w = self.nesteddict_withseq
        assert w.c[0] == w['c'][0]
        assert w.c[0].x == w['c'][0]['x']
        assert w.c[0].y == w['c'][0]['y']
        assert w.c[0].schema == self.schema3.get('c').attr

    def test_sublistoflists(self):
        w = self.nesteddict_withnestedseq
        assert w.c[0] == w['c'][0]
        assert w.c[0][0] == w['c'][0][0]
        assert w.c[0][0].x == w['c'][0][0]['x']
        assert w.c[0][0].y == w['c'][0][0]['y']
        assert w.c[0][0].schema == self.schema4.get('c').attr.attr

class TestOtherAttrs(unittest.TestCase):

    def setUp(self):
       setUp(self) 

    def test_items(self):
        w = self.nesteddict_withseq
        for k,v in w.items():
            assert v == w[k]
            if isinstance(v,dict) or isinstance(v,list):
                assert v.schema == self.schema3.get(k)

    def test_inlist(self):
        w = self.nesteddict_withseq
        schema = w.schema
        for v in w['c']:
            assert v.x == w['c'][0]['x']
            assert v.y == w['c'][0]['y']

    def test_get(self):
        w = self.nesteddict_withseq
        schema = w.schema
        a = w.get('c')
        assert a == w['c']
        assert a.schema == self.schema3.get('c')
        
        
    def test_values(self):
        w = self.nesteddict_withseq
        schema = w.schema
        r = [v for v in w.values()]
        r.sort()
        assert r[0] == 1
        assert r[1] == w['c']
        assert r[2] == w['b']
        assert r[1].schema == self.schema3.get('c')
        assert r[2].schema == self.schema3.get('b')
    
    def test_iteritems(self):
        w = self.nesteddict_withseq
        schema = w.schema
        for k,v in w.iteritems():
            assert v == w[k]
            if isinstance(v,dict) or isinstance(v,list):
                assert v.schema == self.schema3.get(k)

    def test_itervalues(self):
        w = self.nesteddict_withseq
        schema = w.schema
        r = [v for v in w.itervalues()]
        r.sort()
        assert r[0] == 1
        assert r[1] == w['c']
        assert r[2] == w['b']
        assert r[1].schema == self.schema3.get('c')
        assert r[2].schema == self.schema3.get('b')

    def test_pop(self):
        w = copy(self.nesteddict_withseq)
        schema = w.schema
        c = copy(w['c'])
        a = w.pop('c')
        assert a == c
        assert a.schema == self.schema3.get('c')
        ks = w.keys()
        ks.sort()
        assert ks == ['a','b']

    def test_popitem(self):
        w = copy(self.nesteddict_withseq)
        schema = w.schema
        c = copy(('c', w['c']))
        a = w.popitem('c')
        assert a == c
        assert a[1].schema == self.schema3.get('c')
        ks = w.keys()
        ks.sort()
        assert ks == ['a','b']


