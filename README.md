# Little Langs

This demonstrates three languages:

1. Integers and addition.
2. Integers, addition, and variable binding (aka "let").
3. Integers, addition, variable binding, and a syntax.

Exercises for the reader:

1. Can you add Multiply to lang2?
2. Can you add Multiply to lang3?

For the latter, make sure this evaluates to 25 not 70:

    5 + 2 * 10

To run the tests in a file execute it like this:

    python3 -m little_langs.lang1

If you see no errors, then all the tests passed!

You can run the lang3 interpreter on a file like this:

    python3 -m little_langs.run_lang3 little_langs/example.lang3
