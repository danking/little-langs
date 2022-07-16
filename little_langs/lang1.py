# The Plus Language
#
# This is the simplest language. All you get are integers and you can add integers.

class Int:
    def __init__(self, value):
        self.value = value


class Plus:
    def __init__(self, left, right):
        self.left = left
        self.right = right


def interpret(expr):
    if isinstance(expr, Int):
        return expr.value
    if isinstance(expr, Plus):
        left = interpret(expr.left)
        right = interpret(expr.right)
        return left + right
    raise ValueError(f"unknown expr: {expr}")

assert interpret(Int(3)) == 3
assert interpret(Plus(Int(3), Int(5))) == 8
