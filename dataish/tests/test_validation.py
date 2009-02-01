import unittest
from dataish.schema.wrapper import Wrapper
from copy import copy
import schemaish
from validatish import validator as v

import logging as log

log.basicConfig(level=log.DEBUG)

def sS(*items):
    return schemaish.Structure(items)
def SI(name, **k):
    return (name, schemaish.Integer(**k))
def SS(name, items):
    return (name, schemaish.Structure(items))
def SQ(name, schema_type):
    return (name, schemaish.Sequence(schema_type))
def sQ(schema_type):
    return schemaish.Sequence(schema_type)

class TestBasic(unittest.TestCase):


    def test_firstchild(self):
        d = {'a': None, 'b': 2, 'c': 3}
        schema = sS(SI('a', validator=v.Required()),SI('b'),SI('c'))
        w = Wrapper(d, schema)
        try:
            w.validate()
        except schemaish.Invalid, e:
            assert e.message=='field "a" is required'
            

    def test_subchildren(self):
        d = {'a': 1, 'b': {'p':12,'q':None}, 'c': {'x':25,'y': 26}}
        schema = sS(SI('a'),SS('b',[SI('p'),SI('q',validator=v.Required())]),SS('c',[SI('x'),SI('y')]))
        w = Wrapper(d, schema)        
        try:
            w.validate()
        except schemaish.Invalid, e:
            assert e.message=='field "b.q" is required'

        wb = w.b
        try:
            wb.validate()
        except schemaish.Invalid, e:
            assert e.message=='field "q" is required'



