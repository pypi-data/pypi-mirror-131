# This file is placed in the Public Domain.


import unittest


from bot.obj import Object
from bot.ofn import dumps, loads

class Test_JSON(unittest.TestCase):

    def test_json(self):
        o = Object()
        o.test = "bla"
        a = loads(dumps(o))
        self.assertEqual(a.test, "bla")

    def test_jsondump(self):
        o = Object()
        o.test = "bla"
        self.assertEqual(dumps(o), '{"test": "bla"}')
