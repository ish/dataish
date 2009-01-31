import unittest
from dataish.schema.wrapper import Wrapper
from copy import copy

schema = object()


def setUp(self):
    d = {'a': 1, 'b': 2, 'c': 3}
    self.simpledict = Wrapper(d, schema)

    d = {'a': 1, 'b': {'p':12,'q':13}, 'c': {'x':25,'y': 26}}
    self.nesteddict = Wrapper(d, schema)

    d = {'a': 1, 'b': {'p':12,'q':13}, 'c': [{'x':25,'y': 26},]}
    self.nesteddict_withseq = Wrapper(d, schema)

    d = {'a': 1, 'b': {'p':12,'q':13}, 'c': [[{'x':25,'y': 26},],]}
    self.nesteddict_withnestedseq = Wrapper(d, schema)

class TestBasic(unittest.TestCase):

    def setUp(self):
       setUp(self) 


    def test_firstchild(self):
        w = self.simpledict
        assert w.a == w['a']
        assert w.b == w['b']
        assert w.c == w['c']
        assert w.schema == schema

    def test_subchildren(self):
        w = self.nesteddict
        assert w.c == w['c']
        assert w.c.x == w['c']['x']
        assert w.c.y == w['c']['y']
        assert w.c.schema == schema

    def test_sublists(self):
        w = self.nesteddict_withseq
        assert w.c[0] == w['c'][0]
        assert w.c[0].x == w['c'][0]['x']
        assert w.c[0].y == w['c'][0]['y']
        assert w.c[0].schema == schema

    def test_sublistoflists(self):
        w = self.nesteddict_withnestedseq
        assert w.c[0] == w['c'][0]
        assert w.c[0][0] == w['c'][0][0]
        assert w.c[0][0].x == w['c'][0][0]['x']
        assert w.c[0][0].y == w['c'][0][0]['y']
        assert w.c[0][0].schema == schema

class TestOtherAttrs(unittest.TestCase):

    def setUp(self):
       setUp(self) 

    def test_items(self):
        w = self.nesteddict_withseq
        for k,v in w.items():
            assert v == w[k]
            if isinstance(v,dict) or isinstance(v,list):
                assert v.schema == schema

    def test_inlist(self):
        w = self.nesteddict_withseq
        for v in w['c']:
            assert v.x == w['c'][0]['x']
            assert v.y == w['c'][0]['y']

    def test_get(self):
        w = self.nesteddict_withseq
        print w.schema
        a = w.get('c')
        print type(a)
        assert a == w['c']
        assert a.schema == schema
        
        
    def test_values(self):
        w = self.nesteddict_withseq
        r = [v for v in w.values()]
        r.sort()
        assert r[0] == 1
        assert r[1] == w['c']
        assert r[2] == w['b']
        assert r[1].schema == schema
        assert r[2].schema == schema
    
    def test_iteritems(self):
        w = self.nesteddict_withseq
        for k,v in w.iteritems():
            assert v == w[k]
            if isinstance(v,dict) or isinstance(v,list):
                assert v.schema == schema

    def test_itervalues(self):
        w = self.nesteddict_withseq
        r = [v for v in w.itervalues()]
        r.sort()
        print r
        assert r[0] == 1
        assert r[1] == w['c']
        assert r[2] == w['b']
        assert r[1].schema == schema
        assert r[2].schema == schema

    def test_pop(self):
        w = copy(self.nesteddict_withseq)
        c = copy(w['c'])
        print w
        a = w.pop('c')
        assert a == c
        assert a.schema == schema
        ks = w.keys()
        ks.sort()
        assert ks == ['a','b']

    def test_popitem(self):
        w = copy(self.nesteddict_withseq)
        c = copy(('c', w['c']))
        a = w.popitem('c')
        assert a == c
        assert a[1].schema == schema
        ks = w.keys()
        ks.sort()
        assert ks == ['a','b']


