# This file is placed in the Public Domain.

"object functions"

import datetime
import json as js
import os
import types


from .obj import Cfg, Object, ObjectDecoder, ObjectEncoder
from .obj import cdir, items, keys, update

def __dir__():
    return (
        "diff",
        "dump",
        "dumps",
        "edit",
        "fmt",
        "getname",
        "gettype",
        "load",
        "loads",
        "loadp",
        "save",
        "savep"
    )


def diff(o1, o2):
    "difference between 2 objects"
    d = Object()
    for k in keys(o2):
        if k in keys(o1) and o1[k] != o2[k]:
            d[k] = o2[k]
    return d

def dump(o, f):
    return js.dump(o, f, cls=ObjectEncoder)


def dumps(o):
    return js.dumps(o, cls=ObjectEncoder)


def edit(o, setter, skip=True, skiplist=None):
    "change values"
    if skiplist is None:
        skiplist = []
    count = 0
    for key, v in items(setter):
        if skip and v == "":
            del o[key]
        if key in skiplist:
            continue
        count += 1
        if v in ["True", "true"]:
            o[key] = True
        elif v in ["False", "false"]:
            o[key] = False
        else:
            o[key] = v
    return count


def fmt(o, keyz=None, empty=True, skip=None, newline=False):
    "return formatted string"
    if keyz is None:
        keyz = keys(o)
    if not keyz:
        keyz = ["txt"]
    if skip is None:
        skip = []
    res = []
    txt = ""
    for key in keyz:
        if key in skip:
            continue
        if key in dir(o):
            if key.startswith("__"):
                continue
            val = getattr(o, key, None)
            if empty and not val:
                continue
            val = str(val).strip()
            res.append((key, val))
    result = []
    for k, v in res:
        if newline:
            result.append("%s=%s%s" % (k, v, "\n"))
        else:
            result.append("%s=%s%s" % (k, v, " "))
    if newline:
        txt += "\n".join([x.strip() for x in result])
    else:
        txt += " ".join([x.strip() for x in result])
    return txt


def getname(o):
    "return full qualified name"
    t = type(o)
    if isinstance(t, types.ModuleType):
        return o.__name__
    if "__self__" in dir(o):
        return "%s.%s" % (o.__self__.__class__.__name__, o.__name__)
    if "__class__" in dir(o) and "__name__" in dir(o):
        return "%s.%s" % (o.__class__.__name__, o.__name__)
    if "__class__" in dir(o):
        return o.__class__.__name__
    if "__name__" in dir(o):
        return o.__name__
    return None


def gettype(o):
    "return module.class string"
    return str(type(o)).split()[-1][1:-2]


def load(o, opath):
    "load from data store"
    if opath.count(os.sep) != 3:
        return
    assert Cfg.wd
    splitted = opath.split(os.sep)
    stp = os.sep.join(splitted[-4:])
    lpath = os.path.join(Cfg.wd, "store", stp)
    if os.path.exists(lpath):
        with open(lpath, "r") as ofile:
            d = js.load(ofile, cls=ObjectDecoder)
            update(o, d)
    o.__stp__ = stp


def loads(s):
    "decode string to object"
    return js.loads(s, cls=ObjectDecoder)


def loadp(o, opath):
    "load from filesystem"
    assert Cfg.wd
    if os.path.exists(opath):
        with open(opath, "r") as ofile:
            d = js.load(ofile, cls=ObjectDecoder)
            update(o, d)

def indexed(o, txt):
    "push on countered index"
    o.__index__ += 1
    o[str(o.__index__)] = txt


def save(o, tab=False):
    "save to data store"
    assert Cfg.wd
    prv = os.sep.join(o.__stp__.split(os.sep)[:2])
    o.__stp__ = os.path.join(prv,
                             os.sep.join(str(datetime.datetime.now()).split()))
    opath = os.path.join(Cfg.wd, "store", o.__stp__)
    cdir(opath)
    with open(opath, "w") as ofile:
        js.dump(
            o.__dict__, ofile, cls=ObjectEncoder, indent=4, sort_keys=True
        )
    os.chmod(opath, 0o444)
    return o.__stp__

def savep(o, opath, tab=False):
    "save to filesystem"
    #cdir(opath)
    with open(opath, "w") as ofile:
        js.dump(
            o.__dict__, ofile, cls=ObjectEncoder, indent=4, sort_keys=True
        )
    return o.__stp__
