import _illion


def _add_elem(e):
    assert e not in setset._obj2int
    i = len(setset._int2obj)
    _illion.setset(set([i]))
    setset._obj2int[e] = i
    setset._int2obj.append(e)
    assert len(setset._int2obj) == _illion.num_elems() + 1
    assert setset._int2obj[i] == e
    assert setset._obj2int[e] == i

def _hook_args(func):
    def wrapper(self, *args, **kwds):
        if args:
            obj = args[0]
            args = [None] + list(args)[1:]
            if isinstance(obj, (set, frozenset)):
                args[0] = set([_do_hook_args(e) for e in obj])
            elif isinstance(obj, dict):
                args[0] = {}
                for k, l in obj.iteritems():
                    args[0][k] = [_do_hook_args(e) for e in l]
            elif isinstance(obj, list):
                args[0] = []
                for s in obj:
                    args[0].append(set([_do_hook_args(e) for e in s]))
            else:
                args[0] = _do_hook_args(obj)
        return func(self, *args, **kwds)
    return wrapper

def _do_hook_args(e):
    if e not in setset._obj2int:
        _add_elem(e)
    return setset._obj2int[e]

def _hook_ret(func):
    def wrapper(self, *args, **kwds):
        return _do_hook_ret(func(self, *args, **kwds))
    return wrapper

def _do_hook_ret(obj):
    if isinstance(obj, (set, frozenset)):
        ret = set()
        for e in obj:
            ret.add(setset._int2obj[e])
        return ret
    else:
        return setset._int2obj[obj]


class setset_iterator(object):

    def __init__(self, it):
        self.it = it

    def __iter__(self):
        return self

    @_hook_ret
    def next(self):
        return self.it.next()


class setset(_illion.setset):

    @_hook_args
    def __init__(self, *args, **kwds):
        _illion.setset.__init__(self, *args, **kwds)

    def __repr__(self):
        n = _illion.num_elems()
        w = {}
        for i in range(1, n + 1):
            e = setset._int2obj[i]
            w[e] = - (1 + float(i) / n**2)
        ret = self.__class__.__name__ + '(['
        i = 1
        for s in setset.optimize(self, w):
            if i >= 2:
                ret += ', '
            ret += str(s)
            if i >= 4:
                i = -1
                break
            else:
                i += 1
        if i < 0:
            ret += ', ...'
        return ret + '])'

    @_hook_args
    def __contains__(self, *args, **kwds):
        return _illion.setset.__contains__(self, *args, **kwds)

    @_hook_args
    def include(self, *args, **kwds):
        return _illion.setset.include(self, *args, **kwds)

    @_hook_args
    def exclude(self, *args, **kwds):
        return _illion.setset.exclude(self, *args, **kwds)

    @_hook_args
    def add(self, *args, **kwds):
        return _illion.setset.add(self, *args, **kwds)

    @_hook_args
    def remove(self, *args, **kwds):
        return _illion.setset.remove(self, *args, **kwds)

    @_hook_args
    def discard(self, *args, **kwds):
        return _illion.setset.discard(self, *args, **kwds)

    @_hook_ret
    def pop(self, *args, **kwds):
        return _illion.setset.pop(self, *args, **kwds)

    def __iter__(self):
        return setset_iterator(self.rand_iter())

    def randomize(self):
        i = self.rand_iter()
        while (True):
            yield _do_hook_ret(i.next())

    def optimize(self, *args, **kwds):
        default = kwds['weight'] if 'weight' in kwds else 1
        weights = [default] * (_illion.num_elems() + 1)
        if args:
            for e, w in args[0].iteritems():
                i = setset._obj2int[e]
                weights[i] = w
        i = self.opt_iter(weights)
        while (True):
            yield _do_hook_ret(i.next())

    @staticmethod
    def universe(*args):
        if args:
            _illion.num_elems(0)
            setset._obj2int = {}
            setset._int2obj = [None]
            for e in args[0]:
                _add_elem(e)
            setset._check_universe()
        else:
            setset._check_universe()
            return setset._int2obj[1:]

    @staticmethod
    def _check_universe():
        assert len(setset._int2obj) == _illion.num_elems() + 1
        for e, i in setset._obj2int.iteritems():
            assert e == setset._int2obj[i]
        for i in xrange(1, len(setset._int2obj)):
            e = setset._int2obj[i]
            assert i == setset._obj2int[e]

    _obj2int = {}
    _int2obj = [None]