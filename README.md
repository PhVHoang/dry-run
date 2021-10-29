# Dry run

Dry-run a function borrowed from https://github.com/haarcuba/dryable

```python
import os
from typing import Callable

import dryrun


def alternative_func_a():
    print("Run on alternative A")


@dryrun.DryRun(label='labelA')
def func_a(dry_run_function: Callable = alternative_func_a):
    dry_run_function()
    print("Hi I am A")


@dryrun.DryRun(label='labelB')
def func_b():
    print("Hi I am B")


if __name__ == '__main__':
    dryrun.set(os.getenv('DRY_RUN', True), 'labelA')
    dryrun.set(os.getenv('DRY_RUN', False), 'labelB')
    func_a()
    func_b()

>>> Run on alternative A
>>> Hi I am B
```
