![test workflow](https://github.com/tos-kamiya/init_attrs_with_kwargs/workflows/Tests/badge.svg)

init_attrs_with_kwargs
======================

A helper for type-checked command-line argument store.

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