# This file is placed in the Public Domain.


import unittest


from bot.krn import k
from bot.run import Cfg as RunCfg


class Test_Kernel(unittest.TestCase):

    def test_cfg(self):
        self.assertEqual(type(k.cfg), RunCfg)
