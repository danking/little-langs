from .lang1 import Int, Plus

# The Let Language
#
# This also has integers and addition, but adds variables. We can save a value into a variable with
# "Let". We can refer to that value with "Ref". For example:
#
#    Let("x", Int(5), Plus(Ref("x"), Int(7)))
#
# corresponds to the Python:
#
#    x = 5
#    x + 7

class Let:
    def __init__(self, name, value_expr, body_expr):
        self.name = name
        self.value_expr = value_expr
        self.body_expr = body_expr

    def __repr__(self):
        return f'Let({self.name!r}, {self.value_expr}, {self.body_expr})'

    def __eq__(self, other):
        return (isinstance(other, Let) and
                self.name == other.name and
                self.value_expr == other.value_expr and
                self.body_expr == other.body_expr)


class Ref:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'Ref({self.name!r})'

    def __eq__(self, other):
        return (isinstance(other, Ref) and
                self.name == other.name)


class EmptyEnvironment:
    def __init__(self):
        pass

    def lookup_name(self, name):
        raise ValueError(f"no such name: {name}")

    def __repr__(self):
        return f'EmptyEnvironment'


class Environment:
    def __init__(self, name, value, environment):
        self.name = name
        self.value = value
        self.environment = environment

    def lookup_name(self, name):
        if self.name == name:
            return self.value
        return self.environment.lookup_name(name)

    def __repr__(self):
        return f'Environment({self.name!r}, {self.value}, {self.environment})'


def interpret(expr):
    return _interpret(expr, EmptyEnvironment())


def _interpret(expr, environment):
    if isinstance(expr, Int):
        return expr.value
    if isinstance(expr, Plus):
        left = _interpret(expr.left, environment)
        right = _interpret(expr.right, environment)
        return left + right
    if isinstance(expr, Let):
        value = _interpret(expr.value_expr, environment)
        new_environment = Environment(expr.name, value, environment)
        return _interpret(expr.body_expr, new_environment)
    if isinstance(expr, Ref):
        return environment.lookup_name(expr.name)

    raise ValueError(f"unknown expr: {expr}")

assert interpret(Int(3)) == 3
assert interpret(Plus(Int(3), Int(5))) == 8

# think of this like:
#
#    applepie = 3
#    applepie + applepie
#
expression = Let(
    "applepie", Int(3),
    Plus(Ref("applepie"), Ref("applepie"))
)
assert interpret(expression) == 6

expression = Let(
    "applepie", Plus(Int(3), Int(5)),
    Plus(Ref("applepie"), Ref("applepie"))
)
assert interpret(expression) == 16
