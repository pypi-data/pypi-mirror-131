'''
LIBrary for YARE (Yet Another Regular Expression) pattern match


CONTENT

    1. Installation
    2. Help
    3. Introduction
    4. String Patterns
    5. Charset Patterns
    6. Numeric Patterns
    7. TGMK Literals
    8. Compound Patterns
    9. Three Flavors
    10. Exceptions
    11. History

1. INSTALLATION

    $ pip3 install libyare

2. HELP

    $ pydoc libyare

or, from a Python IDE:

    >>> import libyare
    >>> help(libyare)

3. DEFINITIONS

"YARE"  (Yet  Another  Regular Expression) is a regular expression format aimed to be more
readable (even at the cost of being less powerful) than standard regular expressions.

A "pattern" can be:

    • a "simple pattern", which can be:
        • a "string pattern", a classic Unix shell style pattern
        • a "charset pattern", made by:
            • a backquote '`'
            • a single-char classic Unix shell style pattern
        • a "numeric pattern", made by:
            • a comparison operator '=' '>' '<' '>=' '<=' or '<>'
            • an integer (or TGMK, see later) literal
    • a  "compound  pattern",  made combining simple patterns by logical operators '^' '&'
      and ',' and by parentheses '(' and ')'

"Metacharacters" are:

    • '*' '?' '[' and ']', used in string patterns, out of '[...]'
    • '!' and '-', used in string patterns, between '[' and ']'
    • '`' backquote, used at beginning of charset patterns
    • '^' (not) '&' (and) and ',' (or) logical operators in compound patterns
    • '('  and  ')'  parenthesis altering precedence between logical operators in compound
      patterns

4. STRING PATTERNS

A  "string  pattern" is a classic Unix shell style patterns, without extensions introduced
by bash shell, so, for instance, curly braces '{' and '}' have no special meaning.

    • pattern '*' matches any string
    • pattern '?' matches any single char
    • pattern '[ab]' matches 'a' or 'b'
    • pattern '[!a]' matches any single char except 'a' or 'b'
    • pattern '[a-z]' matches any single char between 'a' and 'z'
    • pattern '[!a-z]' matches any single char not between 'a' and 'z'
    • pattern  '[a-z0-9_]'  matches any single char between 'a' and 'z' or between '0' and
      '9' or equal to '_'
    • pattern '[!a-z0-9_]' matches any single char not between 'a' and 'z' and not between
      '0' and '9' and not equal to '_'

For further details, look for instance at the Python3 documentation about fnmatch module.

If  a  metacharacter  must belong to a simple string pattern then it must be quoted by '['
and ']', more exactly:

    • '*' '?' '[' '^' '&' ',' '(' and ')' must always be quoted
    • '!'  and '-' if not between '[' and ']' have no special meaning and don't need to be
      quoted
    • '`'  needs  to  be quoted only in first position inside the simple string pattern in
      order to avoid confusion with charset pattern
    • '<'  '='  and  '>' need to be quoted only in first position inside the simple string
      pattern in order to avoid confusion with numeric pattern
    • ']'  only can't be quoted, but you shouldn't need it because an unmatched ']' has no
      special meaning and doesn't raise a syntax error, as unmatched '[' '(' and ')' do

Some example:

    • pattern '[(]*[)]' matches any string starting with '(' and ending with ')'
    • pattern '[[]*]' matches any string starting with '[' and ending with ']'
    • patterns '[`]*`' and '[`]*[`]' both match any string starting and ending with '`'
    • patterns  '[<]*>'  and  '[<]*[>]' both match any string starting with '<' and ending
      with '>'

You can quote metacharacter '!' too, but not immediately after '['.

    • pattern '[?!]' matches '?' and '!' only
    • pattern '[!?]' matches any character except '?'

You  can  quote  '-'  too,  but immediately after '[' or before ']' only, otherwise it's a
metacharacter denoting a character interval:

    • patterns '[-pr]' and '[pr-]' match '-' 'p' and 'r'
    • pattern '[p-r]' matches 'p' 'q' and 'r'

But '-' stands for itself even after a character interval:

    • pattern '[p-r-x]' matches 'p' 'q' 'r' '-' and 'x'
    • pattern '[p-r-x-z]' matches 'p' 'q' 'r' '-' 'x' 'y' and 'z'

Descending character intervals are not allowed:

    • pattern '[z-a]' raises a syntax error

They  are  only  two  differences  between  patterns  defined  by  fnmatch()/fnmatchcase()
functions in Python3 fnmatch module and patterns accepted by YARE:

    • unmatched  '['  (as  in  pattern 'abc[def') is allowed by fnmatch but is rejected by
      YARE as a syntax error
    • null pattern '' is allowed by fnmatch but is rejected by YARE as a syntax error (see
      in  paragraph  5. COMPOUND PATTERNS for a workaround to match a null string by a not
      null pattern)

Simple string patterns can be case-sensitive or case-insensitive, depending on which match
function you use, see paragraph 6. THREE FLAVOURS.

5. CHARSET PATTERNS

A "charset pattern" contains:

    • a backquote '`'
    • a single-char classic Unix shell style pattern

A  charset  pattern matches a string if all chars in string match single-char classic Unix
shell style pattern.

Example:

    • '`[a-z0-9]' matches any string made of zero or more underscore alphabetic or numeric
      characters

Charset patterns are always case-sensitive.

6. NUMERIC PATTERNS

A "numeric pattern" is made by:

    • a comparison operator (among '=' '<>' '<' '<=' '>' and '>=')
    • an integer literal (or a TGMK literal, see next paragraph)

No other comparison operator (as '==' '!=' '><' '!<' or '!>') is allowed.

    • pattern '=x' matches any string whose numeric value is equal to x
    • pattern '<>x' matches any string whose numeric value is not equal to x
    • pattern '<x' matches any string whose numeric value is less than x
    • pattern '<=x' matches any string whose numeric value is less than or equal to x
    • pattern '>x' matches any string whose numeric value is greater than x
    • pattern '>=x' matches any string whose numeric value is greater than or equal to x

where  x  is  any  integer  literal (or TGMK literal, see next paragraph), so for instance
patterns '>=1024&<2048' and '>=1k&<2k' are equivalent and both match:

    • '1024', '1025' ... '2047', but also:
    • '1K', '1k1' ... '1k1023'

Numeric patterns are always case-insensitive,

7. TGMK LITERALS

"TGMK"  (Tebi-Gibi-Mebi-Kibi)  is  a  human-readable  lossless  case-insensitive 1024-base
integer representation, suitable for bits and bytes.

A "TGMK literal" is a string containing:

    • zero or more leading blanks
    • an optional ('+' or '-') "sign"
    • one or more "1024-base-digits", each made by:
        • a  "mantissa",  a string of one or more decimal digits, representing an unsigned
          decimal integer constant, as '0', '1' or '100000'.
        • a "characteristic", a letter in 'KMGTPEZY' (or 'kmgtpezy', case has no meaning)
    • zero or more trailing blanks

Only last (rightmost) 1024-base-digit can lack characteristic, meaning unities.

Characteristic letters have the following well-known meanings:

    ╔══════╤══════╤════╤═════╤════╤══════════════════╤═══════╤═════════════════════════╗
    ║LETTER│PREFIX│BITS│BYTES│LOG2│      LOG10       │LOG1024│          VALUE          ║
    ╟──────┼──────┼────┼─────┼────┼──────────────────┼───────┼─────────────────────────╢
    ║'K'   │kibi- │Kib │KiB  │10.0│ 3.010299956639812│    1.0│                     1024║
    ║'M'   │mebi- │Mib │MiB  │20.0│ 6.020599913279624│    2.0│                  1048576║
    ║'G'   │gibi- │Gib │GiB  │30.0│ 9.030899869919436│    3.0│               1073741824║
    ║'T'   │tebi- │Tib │TiB  │40.0│12.041199826559248│    4.0│            1099511627776║
    ║'P'   │pebi- │Pib │PiB  │50.0│ 15.05149978319906│    5.0│         1125899906842624║
    ║'E'   │exbi- │Eib │EiB  │60.0│ 18.06179973983887│    6.0│      1152921504606846976║
    ║'Z'   │zebi- │Zib │ZiB  │70.0│21.072099696478684│    7.0│   1180591620717411303424║
    ║'Y'   │yobi- │Yib │YiB  │80.0│24.082399653118497│    8.0│1208925819614629174706176║
    ╚══════╧══════╧════╧═════╧════╧══════════════════╧═══════╧═════════════════════════╝

Characteristic letters must appear left to right in strictly decreasing value order:

    • '3m5k7' is ok, its value is 3 * 1024 ** 2 + 5 * 1024 + 7 == 3150855
    • '5k3m7' is wrong
    • '5k3k7' is wrong too

In mantissas one or more leading zeros are allowed, while commas are not:

    • '04096m' is ok
    • '4,096m' is wrong

For further details, see https://pypi.org/project/libtgmk.

TGMK literals are always case-insensitive, so YARE numeric patterns are too.

8. COMPOUND PATTERNS

In the following examples, p and q are two simple patterns.

A  "compound  pattern"  is built aggregating simple patterns by logic operators '^' (not),
'&' (and) and ',' (or) and parenthesis '(' and ')':

    • pattern '^p' matches any string not matching pattern p
    • pattern 'p&q' matches any string matching both pattern p and pattern q
    • pattern 'p,q' matches any string matching pattern p or pattern q (or both)

Two '^' characters cancel each other out:

    • pattern '^^*z' matches any string ending with 'z'

Precedence is of course '^' > '&' > ',':

    • pattern  '??,^s*&*t' matches any 2-chars string, or any string not starting with 's'
      and ending with 't'
    • pattern '>=10&<13,>20&<=23' matches any int (or TGMK) string worth 10 11 12 21 22 or
      23

But  precedence  can be forced by parenthesis '(' and ')': so for instance, let p and q be
two simple patterns, then De Morgan's laws tell us that:

    • patterns '^p&^q' and '^(p,q)' are equivalent
    • patterns '^p,^q' and '^(p&q)' are equivalent

As  said before, a null pattern '' is not allowed, but if you need to match a null string,
then you can use a workaround:

    • pattern '?*' matches everything, except the null string, so...
    • pattern '^?*' matches the null string, and nothing else

Be  careful  using  '^'  operator  with  charset patterns, for instance the following four
patterns have four distict meanings:

    • '`[0-9]' matches strings containing numeric chars only, hence containing:
        • zero or more numeric chars
        • zero not numeric chars
    • '`[!0-9]' matches strings containing not numeric chars only, hence containing:
        • zero numeric chars
        • zero or more not numeric chars
    • '^`[0-9]' matches strings not containing numeric chars only, hence containing:
        • zero or more numeric chars
        • one or more not numeric chars
    • '^`[!0-9]' matches strings not containing not numeric chars only, hence containing:
        • one or more numeric chars
        • zero or more not numeric chars

9. THREE FLAVOURS

YARE match comes in three flavours:

    • csmatch(string, pattern, case='s') # case-sensitive match
    • cimatch(string, pattern, case='i') # case-insensitive match
    • cxmatch(string, pattern, case='d') # case-mixed match

Of  course  csmatch(string,  pattern, case='i') is equivalent to cimatch(string, pattern),
and so on.

In  case-mixed  match any simple string pattern can be case-sensitive or case-insensitive,
depending on its content:

    • if  the  simple  pattern  contains  one  or  more  lowercase  letters  then match is
      case-sensitive
    • otherwise the match is case-insensitive

Example:

    • pattern 'RAM,?*.db' matches 'ram', 'Ram', 'RAM' or 'xyz.db', but not 'xyz.Db'

A  lowercase letter is any letter having a distinct corresponding uppercase letter, so for
instance 'å' is said to be a lowercase letter because 'å'.upper() == 'Å' != 'å'.

The  three  flavors  only have to do with string patterns because, as said before, charset
patterns are always case-sensitive, and numeric patterns are always case-insensitive.

10. EXCEPTIONS

    • SyntaxError if pattern is not well-formed
    • ValueError if an incorrect TGMK literal is found in pattern
    • ValueError if case is not 's' 'i' or 'x'

Note that if an incorrect TGMK literal is found in string to be matched, then no exception
is raised, but the match returns with a result of False, for example:

    >>> csmatch('3.14', '>3&<4')
    False

because '3.14' contains a dot, so it's not a correct TGMK literal.

11. HISTORY

    • 0.4.1
        • first version published on pypi.org
'''

#----- imports -----

from fnmatch import fnmatchcase
from libtgmk import tgmk2int
from re import error as ReError

#----- constants -----

__version__ = '0.4.1'
__all__ = ['csmatch','cimatch','cxmatch']

PATTERN, LEFT, RIGHT, OR, AND, NOT = '*(),&^' # tokens: patterns and operators

rank_left, rank_right, rank_or, rank_and, rank_not = [0, 0, 1, 2, 3] # operator priorities
rank = {LEFT: rank_left, RIGHT: rank_right, OR: rank_or, AND: rank_and, NOT: rank_not}

after = {OR: frozenset([PATTERN, NOT, LEFT]), # token sequence check
         AND: frozenset([PATTERN, NOT, LEFT]),
         NOT: frozenset([PATTERN, NOT, LEFT]),
         LEFT: frozenset([PATTERN, NOT, LEFT]),
         RIGHT: frozenset([OR, AND, RIGHT]),
         PATTERN: frozenset([OR, AND, RIGHT])}

#----- functions -----

def cimatch(string, pattern, case='i'):
    'case-insensitive YARE match'
    return csmatch(string, pattern, case)

def cxmatch(string, pattern, case='x'):
    'case-mixed YARE match'
    return csmatch(string, pattern, case)

def csmatch(string, pattern, case='s'):
    'case-sensitive YARE match'

    def scanner(pattern):
        '''
translate  {pattern}  into  a  list of {tokens}, checking the correct token sequence, each
token will be an operator or a simple (string or charset or numeric) pattern
'''
        not_in_simple, in_simple, in_brakes = [0, 1, 2] # scanner status values
        tokens = []
        status = not_in_simple
        allowed = LEFT
        for char in LEFT + pattern + RIGHT:
            if status == not_in_simple:
                tokens.append(char)
                if char in rank: # char is an operator
                    assert char in allowed
                    allowed = after[char]
                else: # char starts a simple pattern
                    assert PATTERN in allowed
                    allowed = after[PATTERN]
                    status = in_brakes if char == '[' else in_simple
            elif status == in_simple:
                if char in rank: # char is an operator, simple pattern ends
                    assert char in allowed
                    allowed = after[char]
                    tokens.append(char)
                    status = not_in_simple
                else: # simple pattern continues
                    tokens[-1] += char
                    if char == '[': status = in_brakes
            else: # status == in_brakes, ie between '[' and ']'
                tokens[-1] += char
                if char == ']': status = in_simple
        assert status != in_brakes # unmatched '[' is not allowed
        return tokens

    def match(pattern):
        'match {string} with simple {pattern} by {case}'
        global number
        first = pattern[0]
        if first == '`': # simple charset pattern
            charpattern = pattern[1:]
            return all(fnmatchcase(char, charpattern) for char in string)
        elif '<' <= first <= '>': # if first in '<=>': simple number pattern
            if number is None:
                try:
                    number = tgmk2int(string)
                except:
                    return False
            if first == '<':
                if pattern[:2] == '<>':
                    return number != tgmk2int(pattern[2:])
                elif pattern[:2] == '<=':
                    return number <= tgmk2int(pattern[2:])
                else:
                    return number < tgmk2int(pattern[1:])
            elif first == '>':
                if pattern[:2] == '>=':
                    return number >= tgmk2int(pattern[2:])
                else:
                    return number > tgmk2int(pattern[1:])
            else: # first == '='
                return number == tgmk2int(pattern[1:])
        elif case == 's': # simple string pattern, case sensitive
            return fnmatchcase(string, pattern)
        elif case == 'i': # case insensitive
            return fnmatchcase(string.upper(), pattern.upper())
        elif pattern != pattern.upper(): # case mixed, if (pattern) contain lowercases...
            return fnmatchcase(string, pattern) # ...then case sensitive...
        else:
            return fnmatchcase(string.upper(), pattern) # ...else case insensitive

    def apply(operator):
        'apply {operator} on {values}'
        if operator == OR:
            x = values[-2]
            y = values.pop()
            values[-1] = ((True if x is True else False if x is False else match(x)) or
                          (True if y is True else False if y is False else match(y)))
        elif operator == AND:
            x = values[-2]
            y = values.pop()
            values[-1] = ((True if x is True else False if x is False else match(x)) and
                          (True if y is True else False if y is False else match(y)))
        else: # operator == NOT
            x = values[-1]
            values[-1] = False if x is True else True if x is False else not match(x)

    global number # {string} converted to int...
    number = None # ...but only when it's needed
    operators = [] # operator stack
    values = [] # value stack, each value is str (simple pattern yet to be matched)
                # or bool (simple pattern already matched)
    try: # this is Dijkstra's 'two-stacks' (aka 'shunting-yard') algorithm
        for token in scanner(pattern):
            if token == LEFT:
                operators.append(token)
            elif token == RIGHT:
                while operators and operators[-1] != LEFT: # go back until matching LEFT
                    apply(operators.pop())
                operators.pop() # pop LEFT
            elif token == OR:
                while operators and rank[operators[-1]] >= rank_or: # '>=' for binary operator
                    apply(operators.pop())
                operators.append(token)
            elif token == AND:
                while operators and rank[operators[-1]] >= rank_and: # '>=' for binary operator
                    apply(operators.pop())
                operators.append(token)
            elif token == NOT:
                while operators and rank[operators[-1]] > rank_not: # '>' for unary operator
                    apply(operators.pop())
                operators.append(token)
            else: # token is a simple pattern
                values.append(token)
        assert not operators and len(values) == 1
        x = values[0]
        return True if x is True else False if x is False else match(x)
    except (AssertionError, IndexError, ReError):
        raise SyntaxError(f'syntax error in {pattern!r} YARE pattern')
