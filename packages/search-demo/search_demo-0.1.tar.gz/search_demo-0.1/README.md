# Search Demo
Extremely simple python-curses search demo that runs a function on every
character input and shows / returns the results.

Install using pip!
`pip install search-demo`

## How to use
This assumes that you have a function that outputs an iterable (list, tuple,
etc.) and takes in a string.

```py
from search_demo import SearchDemo

def function(inp):
    return inp.split()

s = SearchDemo(function)
print(s.run_demo())
```

Produces something like this

[![asciicast](https://asciinema.org/a/akVUAsf7MznJQdmjs7VVYwHFO.svg)](https://asciinema.org/a/akVUAsf7MznJQdmjs7VVYwHFO)

## Why
I made this for a part of my masters project that required demoing a
full text search using RediSearch and thought that a small curses library would
be the best way to show it off without too much complexity building a whole UI.

## Note
Please do not use this in real code, I just thought it was useful enough to
share with anyone else who needs a quick demo.
