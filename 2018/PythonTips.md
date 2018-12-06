# re.findall

Finds all the non-overlapping matches for a regular expression in a
string. Useful for extracting all the integers, for instance, from a
line of input.

```
>>> re.findall(r'-?\d+', '12/6/2018 08:19 @33,44 128')
['12', '6', '2018', '08', '19', '33', '44', '128']
```


# namedtuple

See https://docs.python.org/3/library/collections.html#collections.namedtuple

Generates a tuple "struct" with named fields in addition to indexed fields.

From the Python docs:

```
>>> # Basic example
>>> Point = namedtuple('Point', ['x', 'y'])
>>> p = Point(11, y=22)     # instantiate with positional or keyword arguments
>>> p[0] + p[1]             # indexable like the plain tuple (11, 22)
33
>>> x, y = p                # unpack like a regular tuple
>>> x, y
(11, 22)
>>> p.x + p.y               # fields also accessible by name
33
>>> p                       # readable __repr__ with a name=value style
Point(x=11, y=22)
```
