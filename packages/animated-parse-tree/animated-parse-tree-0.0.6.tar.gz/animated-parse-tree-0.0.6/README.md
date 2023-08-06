# Animated Parse Tree

|               |                   |
|---------------|-------------------|
|   Author      |   Ethan Tan       |
|   Date        |   11/12/2021      |
|   Language    |   Python (py)     |

## Description

This package is meant to provide a high-level API for programmers to visualise parse trees. The eventual goal is to animate the tokenization (extracting symbols from a string), lexing (formatting the tokens), parsing (building the parse tree) and evaluation (reducing the parse tree).

## Setup

It is extremely easy to integrate this package in your existing projects.

In the command line, run:

```console
pip install animated_parse_tree
```

## Sample Usage

Then in your Python source file / Jupyter Notebook, insert:

```python
from animated_parse_tree import ParseTree

# Instantiate Parse Tree Object
t = ParseTree()

# Read a Mathematical String Expression (separated by singular whitespace characters)
t.read('1 + 2 * 3')

# Retrieve the Result
print('<<< Equation >>>')
print(t.expression, '=', t.evaluate(), end='\n\n')

# Display the Parse Tree
print('<<< Parse Tree >>>')
print(str(t))
```

The output in the terminal will look something like this:

```console
<<< Equation >>>
1 + 2 * 3 = 7.0

<<< Parse Tree >>>
   +
 ↙     ↘
1.0    *
     ↙   ↘
    2.0 3.0
```

## Declaring Custom Operands/Operators

Refer to `bundles.py`

## See Also