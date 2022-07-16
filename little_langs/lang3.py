from .lang3_ast import Int, Plus, Let, Ref, interpret

# A "Syntax" for the Let Language
#
# You're probably thinking: hey dan, this isn't a "programming" langauge, its just some Python
# classes. I disagree, but you probably would be happier if our progrmming language had syntax.
#
# A "syntax" refers to the representation of our language in text: letters, numbers, spaces,
# punctuation, etc. Our classes thus far, Int, Plus, Let, and Ref, are usually called "abstract
# syntax" or "AST nodes".
#
# Converting syntax into abstract syntax is called "parsing" and its one of the hardest parts of
# writing a new language!
#
# Let's write a very simple syntax for our language:
#
# 1. Integers are just sequences of digits.
#
# 2. Variable names are sequences of letters.
#
# 3. "variable = expression" on its own line means set the variable to the value of the expression
#
# 4. "e1 + e2" means add e1 to e2
#
# 5. A program is:
#    - zero or more "variable = expression" lines, followed by
#    - exactly one line that is either an integer, or one or more additions.
#
# For example:
#
#     3
#
# or
#
#     3 + 4
#
# or
#
#     x = 3
#     y = 4
#     z = x + y
#     z + z + z


def parse(s):
    lines = s.split("\n")
    if len(lines) == 0:
        raise ValueError("empty program!")
    return parse_line(lines[0], lines[1:])


def parse_line(line, rest_of_lines):
    line = line.strip()  # remove whitespace
    if "=" in line:
        parts = line.split("=")
        if len(parts) != 2:
            raise ValueError(f"bad variable assignment: {line}")
        variable = parts[0].strip()
        expression = parts[1].strip()
        if len(rest_of_lines) == 0:
            raise ValueError(f"missing body after variable assignment! {line}")
        parsed_expression = parse_plus_integer_or_variable(expression)
        return Let(
            variable,
            parsed_expression,
            parse_line(rest_of_lines[0], rest_of_lines[1:])
        )
    # else, must be an integer, variable, or plus
    if len(rest_of_lines) != 0:
        raise ValueError(f"only one line allowed after variable assignments, but found: {line} and {rest_of_lines}")
    return parse_plus_integer_or_variable(line)


def parse_plus_integer_or_variable(expr):
    if "+" in expr:
        integers_or_variables = expr.split("+")
        parsed_integers_or_variables = [parse_integer_or_variable(x) for x in integers_or_variables]
        if len(parsed_integers_or_variables) == 1:
            raise ValueError(f"found a + with only a left-hand-side? {expr}")

        one_or_more_plusses = Plus(parsed_integers_or_variables[0], parsed_integers_or_variables[1])
        for integer_or_variable in parsed_integers_or_variables[2:]:
            one_or_more_plusses = Plus(one_or_more_plusses, integer_or_variable)
        return one_or_more_plusses
    # else, must be just an integer or variable
    return parse_integer_or_variable(expr)


def parse_integer_or_variable(s):
    s = s.strip()  # remove whitespace
    if any(x in s for x in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")):
        try:
            return Int(int(s))
        except ValueError as err:
            raise ValueError(f"expected an integer: {s}") from err
    # else, it is a variable name
    return Ref(s)


actual = parse("3")
expected = Int(3)
assert actual == expected, actual

actual = parse("3 + 4")
expected = Plus(Int(3), Int(4))
assert actual == expected, actual

actual = parse("""x = 3
y = 4
z = x + y
z + z + z""")
expected = Let("x", Int(3), Let("y", Int(4), Let("z", Plus(Ref("x"), Ref("y")), Plus(Plus(Ref("z"), Ref("z")), Ref("z")))))
assert actual == expected, actual


assert interpret(parse("3")) == 3
assert interpret(parse("3 + 4")) == 7
assert interpret(parse("""x = 3
y = 4
z = x + y
z + z + z""")) == 21
assert interpret(parse("""x = 3
x = 15
x + x""")) == 30


def parse_and_interpret(s):
    return interpret(parse(s))
