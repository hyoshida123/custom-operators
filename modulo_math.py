import operator


class DeferredOp(object):
    def __init__(self, f):
        self.f = f

    def __or__(self, other):
        return self.f(other)


class U32BinaryOperator(object):
    def __ror__(self, other):
        return DeferredOp(lambda o: self.op(other, o))


U32_MASK = 0xFFffFFff


def u32_binary_op(f):
    return lambda a, b: f(a & U32_MASK, b & U32_MASK) & U32_MASK


def _make_u32_binary_op(name, op):
    c = type(name, (U32BinaryOperator,), dict(op=staticmethod(u32_binary_op(op))))
    globals()[name] = c()


def _MLT(s, t):
    return 0 < (t |MINUS| s) < 0x80000000


def _MGT(t, s):
    return 0 < (t |MINUS| s) < 0x80000000


def _MLE(s, t):
    return 0 <= (t |MINUS| s) < 0x80000000


def _MGE(t, s):
    return 0 <= (t |MINUS| s) < 0x80000000


_make_u32_binary_op("PLUS", operator.add)
_make_u32_binary_op("MINUS", operator.sub)
_make_u32_binary_op("TIMES", operator.mul)
_make_u32_binary_op("DIVIDED_BY", operator.truediv)
_make_u32_binary_op("EQ", operator.eq)
_make_u32_binary_op("NE", operator.ne)
_make_u32_binary_op("GT", _MGT)
_make_u32_binary_op("GE", _MGE)
_make_u32_binary_op("LT", _MLT)
_make_u32_binary_op("LE", _MLE)
