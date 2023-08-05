# This file is placed in the Public Domain.

"Big O Object class"

import datetime
import json as js
import os
import pathlib
import uuid


def __dir__():
    return (
        "Object",
        "cdir",
        "dump",
        "dumps",
        "get",
        "gettype",
        "hook",
        "indexed",
        "keys",
        "loads",
        "items",
        "register",
        "search",
        "set",
        "update",
        "values",
    )


counter = 0


def cdir(path):
    "create directory"
    if os.path.exists(path):
        return
    if path.split(os.sep)[-1].count(":") == 2:
        path = os.path.dirname(path)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


class NoPickle(Exception):

    "we don't do pickle"


class Object:

    "Big O Object class"

    __slots__ = (
        "__dict__",
        "__stp__",
        "__otype__",
        "__index__"
    )

    def __init__(self):
        super().__init__()
        self.__otype__ = str(type(self)).split()[-1][1:-2]
        self.__stp__ = os.path.join(
            self.__otype__,
            str(uuid.uuid4()),
            os.sep.join(str(datetime.datetime.now()).split()),
        )
        self.__index__ = 0

    def __contains__(self, k):
        if k in keys(self):
            return True
        return False

    def __delitem__(self, k):
        if k in self:
            del self.__dict__[k]

    def __eq__(self, o):
        return len(self) == len(o)

    def __getitem__(self, k):
        return self.__dict__[k]

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __le__(self, o):
        return len(self) <= len(o)

    def __lt__(self, o):
        return len(self) < len(o)

    def __ge__(self, o):
        return len(self) >= len(o)

    def __gt__(self, o):
        return len(self) > len(o)

    def __hash__(self):
        return id(self)

    def __reduce__(self):
        raise NoPickle

    def __reduce_ex__(self, k):
        raise NoPickle

    def __setitem__(self, k, v):
        self.__dict__[k] = v

    def __oqn__(self):
        return "<%s.%s object at %s>" % (
            self.__class__.__module__,
            self.__class__.__name__,
            hex(id(self)),
        )

    def __str__(self):
        return str(self.__dict__)


class ObjectEncoder(js.JSONEncoder):

    "encode to a writable string"

    def default(self, o):
        if isinstance(o, dict):
            return o.items()
        if isinstance(o, Object):
            return vars(o)
        if isinstance(o, list):
            return iter(o)
        if isinstance(o,
                      (type(str), type(True), type(False),
                       type(int), type(float))):
            return o
        try:
            return js.JSONEncoder.default(self, o)
        except TypeError:
            return repr(o)


class ObjectDecoder(js.JSONDecoder):

    "create object from string"

    @staticmethod
    def decode(s, _w=None):
        o = Object()
        v = js.loads(s)
        update(o, v)
        return o


class Cfg(Object):

    "basic config"

    wd = ".bot"


def get(self, key, default=None):
    "return value"
    return self.__dict__.get(key, default)


def indexed(self, obj):
    "push on countered index"
    global counter
    counter += 1
    self[str(counter)] = obj


def items(self):
    "return dict like items"
    try:
        return self.__dict__.items()
    except AttributeError:
        return self.items()


def keys(self):
    "return dict like keys"
    return self.__dict__.keys()



def register(self, k, v):
    "register key/value"
    self[str(k)] = v


def search(self, s):
    "see if (stringed) values contains s"
    ok = False
    for k, v in items(s):
        vv = getattr(self, k, None)
        if v not in str(vv):
            ok = False
            break
        ok = True
    return ok


def set(self, key, value):
    "set key/value"
    self.__dict__[key] = value


def update(self, data):
    "do dict like update"
    try:
        self.__dict__.update(vars(data))
    except TypeError:
        self.__dict__.update(data)
    return self


def values(self):
    return self.__dict__.values()
