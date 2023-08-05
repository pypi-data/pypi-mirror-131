# This file is placed in the Public Domain.


import unittest


from bot.clt import Client
from bot.krn import k
from bot.obj import Cfg, Object, get, indexed
from bot.run import Runtime
from bot.tbl import Table


events = []


param = Object()
param.add = ["test@shell", "bart", ""]
param.cfg = ["nick=botje", "server=localhost", ""]
param.dlt = ["root@shell"]
param.dne = ["test4", ""]
param.dpl = ["reddit title,summary,link"]
param.flt = ["0", ""]
param.fnd = ["cfg", "log", "rss", "cfg server==localhost", "rss rss==reddit"]
param.log = ["test1", ""]
param.met = ["root@shell"]
param.nck = ["botje"]
param.pwd = ["bart blabla"]
param.rem = ["reddit", ""]
param.rss = ["https://www.reddit.com/r/python/.rss"]
param.tdo = ["things todo"]


import bot.all


class Test_Commands(unittest.TestCase):

    def test_commands(self):
        cmds = list(Table.modnames)
        c = k.first()
        if not c:
            c = Client()
            k.add(c)
        for cmd in reversed(sorted(cmds)):
            for ex in getattr(param, cmd, [""]):
                e = c.event(cmd + " " + ex)
                k.dispatch(e)
                cmdstr = cmd + " " + ex
                events.append(e)
