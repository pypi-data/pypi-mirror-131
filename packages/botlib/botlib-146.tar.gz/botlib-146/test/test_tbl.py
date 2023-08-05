# This file is placed in the Public Domain.


import unittest


from bot.obj import Cfg, Object, values
from bot.ofn import dumps


class Test_Table(unittest.TestCase):

    def test_tblclasses(self):
        import bot.all
        from bot.tbl import Table
        self.assertTrue(Object in values(Table.classes))

