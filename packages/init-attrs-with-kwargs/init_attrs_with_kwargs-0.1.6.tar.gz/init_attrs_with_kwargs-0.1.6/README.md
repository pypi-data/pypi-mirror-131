![test workflow](https://github.com/tos-kamiya/init_attrs_with_kwargs/workflows/Tests/badge.svg)

init_attrs_with_kwargs
======================

A helper for type-checked command-line argument store.

`init_args_with_kwargs` enables to store the command line arguments (positioned arguments and options) parsed with `docopt` in an object of a typed class.

## Sample

```python
from init_attrs_with_kwargs import InitAttrsWKwArgs

class MyArgs(InitAttrsWKwArgs):
    count: int
    name: str
    max_length: int

# Initialize from docopt's return value, with casting str to int
args: MyArgs = MyArgs(_cast_str_values=True, **{'<count>': '1', '--name': "Joe", '--max-length': '100'})

print("args.count=%s" % repr(args.count))
print("args.name=%s" % repr(args.name))
print("args.max_length=%s" % repr(args.max_length))
```

### Another samples:

* [sample1.py](https://github.com/tos-kamiya/init_attrs_with_kwargs/blob/main/sample1.py). Describes data type conversion and error handling.
* [sample2.py](https://github.com/tos-kamiya/init_attrs_with_kwargs/blob/main/sample2.py). Storing `docopt`-parsed command line arguments in a type-hinted class's object.

## Motivation

I like to use docopt to design command lines.
With docopt, I can design a command line in a vague state at first, and then I can make it more and more concrete and detailed.

As a recent trend in Python coding, you can also use type hints for code completion in text editors such as VSCode.
Here's the problem: since the result of docopt parsing is a dictionary, you will be accessing, for example, args["name"], and the editor's completion will not work. Similarly, you cannot benefit from static type checking with type hints.

This issue can be solved by converting a docopt dictionary into an object of a typed class.
`init_attrs_with_kwargs` is a helper just for this purpose.
