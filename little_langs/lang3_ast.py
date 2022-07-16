# Redefine our classes, but now with a string "repr"esentation and a notion of equality. This makes
# debugging and testing easier.

class Int:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'Int({self.value})'

    def __eq__(self, other):
        return (isinstance(other, Int) and
                self.value == other.value)


class Plus:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f'Plus({self.left}, {self.right})'

    def __eq__(self, other):
        return (isinstance(other, Plus) and
                self.left == other.left and
                self.right == other.right)

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
