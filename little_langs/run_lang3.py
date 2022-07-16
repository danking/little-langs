import sys
from .lang3 import parse_and_interpret

if len(sys.argv) != 2:
    print("""wrong number of arguments

Example:

    python3 -m little_langs.run_lang3 my_file.lang3
""")
    sys.exit(1)

filename = sys.argv[1]
file_as_string = open(filename).read()
print(parse_and_interpret(file_as_string))
