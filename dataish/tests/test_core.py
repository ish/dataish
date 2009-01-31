import unittest
from dataish.core.wrapper import Wrapper
from copy import copy


def setUp(self):
    d = {'a': 1, 'b': 2, 'c': 3}
    self.simpledict = Wrapper(d)

    d = {'a': 1, 'b': {'p':12,'q':13}, 'c': {'x':25,'y': 26}}
    self.nesteddict = Wrapper(d)

    d = {'a': 1, 'b': {'p':12,'q':13}, 'c': [{'x':25,'y': 26},]}
    self.nesteddict_withseq = Wrapper(d)

    d = {'a': 1, 'b': {'p':12,'q':13}, 'c': [[{'x':25,'y': 26},],]}
    self.nesteddict_withnestedseq = Wrapper(d)

class TestBasic(unittest.TestCase):

    def setUp(self):
       setUp(self) 


    def test_firstchild(self):
        w = self.simpledict
        assert w.a == w['a']
        assert w.b == w['b']
        assert w.c == w['c']

    def test_subchildren(self):
        w = self.nesteddict
        assert w.c == w['c']
        assert w.c.x == w['c']['x']
        assert w.c.y == w['c']['y']

    def test_sublists(self):
        w = self.nesteddict_withseq
        assert w.c[0] == w['c'][0]
        assert w.c[0].x == w['c'][0]['x']
        assert w.c[0].y == w['c'][0]['y']

    def test_sublistoflists(self):
        w = self.nesteddict_withnestedseq
        assert w.c[0] == w['c'][0]
        assert w.c[0][0] == w['c'][0][0]
        assert w.c[0][0].x == w['c'][0][0]['x']
        assert w.c[0][0].y == w['c'][0][0]['y']

class TestOtherAttrs(unittest.TestCase):

    def setUp(self):
       setUp(self) 

    def test_items(self):
        w = self.nesteddict_withseq
        for k,v in w.items():
            assert v == w[k]

    def test_inlist(self):
        w = self.nesteddict_withseq
        for v in w['c']:
            assert v.x == w['c'][0]['x']
            assert v.y == w['c'][0]['y']

    def test_get(self):
        w = self.nesteddict_withseq
        assert w.get('a') == w['a']
        
    def test_values(self):
        w = self.nesteddict_withseq
        r = [v for v in w.values()]
        r.sort()
        assert r[0] == 1
        assert r[1] == w['c']
        assert r[2] == w['b']
    
    def test_iteritems(self):
        w = self.nesteddict_withseq
        for k,v in w.iteritems():
            assert v == w[k]

    def test_itervalues(self):
        w = self.nesteddict_withseq
        r = [v for v in w.itervalues()]
        r.sort()
        assert r[0] == 1
        assert r[1] == w['c']
        assert r[2] == w['b']

    def test_pop(self):
        w = copy(self.nesteddict_withseq)
        c = copy(w['c'])
        a = w.pop('c')
        assert a == c
        ks = w.keys()
        ks.sort()
        assert ks == ['a','b']

    def test_pop(self):
        w = copy(self.nesteddict_withseq)
        c = copy(('c', w['c']))
        a = w.popitem('c')
        assert a == c
        ks = w.keys()
        ks.sort()
        assert ks == ['a','b']
