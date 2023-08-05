missing_diff_lines
==================

Run `missing_diff_lines()` after you ran `coverage.py`
in a git-repo, e.g. with `coverage run -m unittest discover`. 
It will output a set with tuples in the form `(filename, line-number)`
for every line in the current diff, that has no test that
covers it.

## Example

Say you have this code in `calc.py` and no tests yet:

```
def mul(a, b):
    return a * b
```

You add some more cod:

```
def mul(a, b):
    return a * b

def div(a, b):
    if b == 0:
        return 0
    return a / b

```

As well as a test-suite:
```
class TestDiv(TestCase):

    def test_simple_div(self):
        self.assertEqual(3, div(9, 3))
```

Note, that the branch `b == 0` is not covered. 
And indeed. if you run:

```
$ coverage run -m unittest discover && python3 report.py
```

Where this is the content of `report.py`:
```
from missing_diff_lines import missing_diff_lines
from pprint import pprint

print(missing_diff_lines())
```

You get
```
{('calc.py', 6)}
```

Which is correct, as this line is not covered. But note, that 
the not covered line 2 is not in the current diff and thus is 
not reported. This is the very purpose of this package.