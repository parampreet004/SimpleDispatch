# Simple Dispatch

A library inspired by the Django Dispatch System for simple pub-sub interactions. it is a low footprint 
and small library designed for resource constrained or high-efficiency systems with no dependencies.

## Getting Starting 

To install, `pip install simple-dispatch` or `pipenv install simple-dispatch`

## Usage

### Simple Example
```python
from simple_dispatch import subscriber, dispatch

MY_EVENT = 'abc'

@subscriber(MY_EVENT)
def handle(**kwargs):
    print(kwargs)

def main():
    dispatch(MY_EVENT, a=1, b=2, c=3)

main()

# OUTPUT: {'a': 1, 'b': 2, 'c': 3}
```

### Subscriber Listens to Multiple Events

```python
from simple_dispatch import subscriber, dispatch

MY_EVENT = 'abc'
MY_SECOND_EVENT = 'xyz'

@subscriber(MY_EVENT, MY_SECOND_EVENT)
def handle(**kwargs):
    print(kwargs)

def main():
    dispatch(MY_EVENT, a=1, b=2, c=3)
    dispatch(MY_SECOND_EVENT, a=4, b=5, c=6)

main()

# OUTPUT: 
# {'a': 1, 'b': 2, 'c': 3}
# {'a': 4, 'b': 5, 'c': 6}
```