# This file is in the Public Domain.


import sys


def getobj(mn, on):
    mod = sys.modules.get(mn, None)
    if mod:
        return getattr(mod, on, None)


def spl(txt):
    return [x for x in txt.split(",") if x]
