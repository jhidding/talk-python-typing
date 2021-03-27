---
title: Python Typing
subtitle: safer code and type driven design
author: Johan Hidding
---

# About types

## Static typing (versus dynamic typing)
- Everything has a type, so what is a type?
- Dynamic: any information on a broader catagory that contains a live object
    - The number `4` is an integer between `1` and `10`.
    - The string `"aoeui"` is a sequence of unique characters containing only vowels.
- Static: any information on a broader catagory that **should** contain the object once its live

## Typing versus testing
- Encodes reasoning behind a program. 
- A **fully typed** program gives a **proof** of its correct implementation.

::: {style="font-size: smaller;"}
> One good type is worth 1000 unit tests!<br>
> (actually, 1000 may not be enough ...)
:::

## Context
- Data types in C: `char`, `*float`, `int (*)(double)`
    - Mapping information to raw bits
    - **must** for compiled languages (even implicit)!
- Generic types:
    - Compile time type variables
    - What does the function: `id :: a -> a` do?
    - Interfaces / Classes / Constraints
- Type inference:
    - Apply static type to untyped expressions

## Math of types
- Product types: `A x B`
    - everything `struct`-like
    - `tuple` (unnamed structs)
- Sum types: `A | B`
    - C++: `std::variant`
    - Rust: `enum`
    - TypeScript: `|`
- Map types: `A -> B`
    - C++: `std::function<B (A)>`
    - rust: `fn(A) -> B`
    - TypeScript: `(foo: A): B`

# Why?

## Why Python?
- popular
- wide spread (many domains)
- user friendly (?)
- rise of data science

::: {.notes}
It is always a good idea to remind ourselves why we are using Python, in spite of all its imperfections.

Python is an immensely popular language, used in many domains. It is perceived to be accessible to users who are otherwise not trained as computer scientists. The focus lies on Python being a glue language to tie different functional components together. However, Python has gained traction as an explorative prototyping data-science language, where libraries like NumPy, PyTorch, Pandas, Scipy etc, provide ways to be reasonably efficient for applications that were previously the sole domain of lower level languages like C and Fortran.
:::

## Why types?
- Manage complexity
- Cleaner code
- Catch errors early
- More meaningful error messages

::: {.notes}
With the growth of complexity of Python programming also rises the need of better software development practices: training developers to write cleaner, more readable and more robust code. Having a type system will help to write better code, catch errors early, and get more meaningful debugging messages.
:::

## Sily Example: Do we have a problem?

``` {.python .repl}
def add(a, b):
    return a + b
```

``` {.python .eval #repl}
add(3, 4)
```

## We can also add strings!

``` {.python .eval #repl}
add("Hello, ", "World!")
```

## So what?

``` {.python .eval #repl}
add("Hello, ", 42)
```

# Types in Python

---

We have *duck* typing...

::: {.notes}
Bad code design was (and is) actively promoted by the Python community. By quoting the Zen of Python or asserting to the argument by cuteness (similar to argument by authority) of what is considered Pythonic and what not, some of the coding practices in Python have taken on a religious tone. The idea of duck typing is fundamentally bad. The idea is that we **assume** that an object supports a certain behaviour (thus allowing functions over generic types) and only complain later. The error message that we got for our `add()` function read
:::

## Error!

```
Traceback:
  ... pile of unreadable stack trace ...
  File "<stdin>", line 2, in add
TypeError: can only concatenate str (not "int") to str
```

- The `add()` function is not at fault here! 

## Fix add?

``` {.python}
def add(a, b):
    """Tries to add a and b, returns None otherwise."""
    try:
        return a + b
    except TypeError:
        return None
```

## Religion
To add a bit of religion to the existing canon:

> Catch errors as early as possible

and

> Keep the logic in a code free of boiler plate

::: {.notes}
We took an important function implementing the core inner logic of an application and dirtied it with a `try/except` block. This makes the code less readable. This is also why we love NumPy. Typing in Python lets us express the type constraints of our code statically, increasing safety, robustness and readability in one fell swoop!

Important PEPs: 484, 526, 544
:::

## PEP 484
::: {.notes}
Python 3.5 added support for type hints. The idea of this feature is that types only give hints about the correct arguments to a function.
:::

``` {.python}
def greeting(name: str) -> str:
    return "Hello, " + name
```

- We can now annotate our `add()` function:

``` {.python #add-int}
def add(a: int, b: int) -> int:
    return a + b
```

---

``` {.python #add-ints action=mypy}
add(3, 4)
# Passes MyPy
```

``` {.python #add-strings-instead action=mypy}
add("Hello, ", "World!")
# Does not pass MyPy!
```

## Product types

``` {.python}
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float
```

or

``` {.python}
from typing import Tuple

# Python <=3.8
Point = Tuple[float, float]
# Python >=3.9 (old style will give warning)
Point = tuple[float, float]
```

## Sum types

``` {.python}
from typing import Union

Number = Union[int, float, complex]
```

``` {.python}
from typing import Optional

x: Optional[int] = None
if x is None:
    x = 10
```

## Map types

``` {.python file=examples/float_format.py}
from typing import Callable

FloatFormatter = Callable[[float], str]

my_format: FloatFormatter = "{:.4}".format
```

``` {.python}
from typing import Mapping

Settings = Mapping[str, float]

settings: Settings = {
    "c": 3e8,
    "h_bar": 1.05e-34,
    "G": 6.7e-11
}
```

## Parametric types
Many data structures have type arguments. The following syntax only works in Python &ge; 3.9.

``` {.python file=examples/parametric.py}
def word_lengths(words: list[str]) -> list[int]:
    return [len(w) for w in words]

words = "The quick brown fox jumps over the lazy dog".split()
print(word_lengths(words))
print(word_lengths(w.upper() for w in words))  # fails
```

## Protocol types

``` {.python file=examples/generic.py}
from typing import (Iterable)

def word_lengths(words: Iterable[str]) -> Iterable[int]:
    return (len(w) for w in words)

words = "The quick brown fox jumps over the lazy dog".split()
print(word_lengths(words))
print(word_lengths(w.upper() for w in words))  # passes
```

## Defining your own protocols

``` {.python file=examples/addable.py}
from typing import Protocol, TypeVar

TAdd = TypeVar("TAdd", bound="Addable")

class Addable(Protocol):
    def __add__(self: TAdd, other: TAdd) -> TAdd:
        ...

T = TypeVar("T", bound="Addable")
def add(a: T, b: T) -> T:
    return a + b

print(add("Hello, ", "World!"))
print(add(3, 4))
print(add("hello", 5)) #fails
```


## Data classes

``` {.python}
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float
```

## Generic types

``` {.python}
from typing import (Generic, TypeVar)

T = TypeVar("T")

@dataclass
class Point(Generic[T]):
    x: T
    y: T
```

## Forward type references

``` {.python}
from __future__ import annotations
```

## Recursive types

``` {.python file=examples/tree.py #trees}
from dataclasses import dataclass
from typing import (TypeVar, Generic, Optional, Union)

T = TypeVar("T")

@dataclass
class Tree(Generic[T]):
    value: T
    left: Optional[Tree[T]] = None
    right: Optional[Tree[T]] = None
```

---

``` {.python #trees}
x = Tree(1, left=Tree(2, right=Tree(3)), right=Tree(4))

y = Tree(1, 
         left=Tree(2, right=Tree(3)), 
         right=Tree("hello"))  # fails: cannot deduce type

z: Tree[Union[int, str]] \
    = Tree(1,
           left=Tree(2, right=Tree(3)),  
           right=Tree("hello")) # passes
```

## Setting up MyPy

- Example `setup.cfg`

  ``` {.ini file=setup.cfg}
  [mypy]
  python_version = 3.9
  warn_return_any = True
  warn_unused_configs = True
  
  [mypy-numpy]
  ignore_missing_imports = True
  ```

- Use `pytest-mypy` to integrate with `pytest`.

# A New Python

## Type driven design
- Type annotations
- Dataclasses
- Python 3.10: Pattern matching

> Start by translating your concepts into types

## Example: Building a physics integrator

``` {.python file=examples/integrator.py #pendulum}
from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, TypeVar, Callable, Iterable, Generic
import numpy as np

Vector = TypeVar("Vector", bound="VectorProtocol")

class VectorProtocol(Protocol):
    def __add__(self: Vector, other: Vector) -> Vector: ...
    def __rmul__(self: Vector, other: float) -> Vector: ...
```

-----

``` {.python #pendulum}
class HamiltonianSystem(Protocol[Vector]):
    def momentumEquation(self, s: State[Vector]) -> Vector: ...
    def positionEquation(self, s: State[Vector]) -> Vector: ...
```

-----

``` {.python #pendulum}
@dataclass
class State(Generic[Vector]):
    time: float
    position: Vector
    momentum: Vector

    def kick(self, dt: float, h: HamiltonianSystem[Vector]) -> State[Vector]:
        self.momentum += dt * h.momentumEquation(self)
        return self

    def drift(self, dt: float, h: HamiltonianSystem[Vector]) -> State[Vector]:
        self.position += dt * h.positionEquation(self)
        return self

    def wait(self, dt: float) -> State[Vector]:
        self.time += dt
        return self
```

-----

``` {.python #pendulum}
Solver = Callable[[HamiltonianSystem[Vector], State[Vector]], State[Vector]]
Stepper = Callable[[State[Vector]], State[Vector]]
HaltingCondition = Callable[[State[Vector]], bool]

def leap_frog(dt: float, h: HamiltonianSystem[Vector], s: State[Vector]) -> State[Vector]:
    return s.kick(dt, h).wait(dt/2).drift(dt, h).wait(dt/2)

def iterate_step(step: Stepper, halt: HaltingCondition, init: State[Vector]) -> Iterable[State[Vector]]:
    state = init
    while not halt(state):
        state = step(state)
        yield state

def halt_at_time(t: float) -> HaltingCondition:
    return lambda s: s.time >= t

@dataclass
class IdealPendulum:
    mass: float
    length: float

    def momentumEquation(self, s: State[float]) -> float:
        return - self.mass * self.length * 9.81 * float(np.sin(s.position))

    def positionEquation(self, s: State[float]) -> float:
        return s.momentum / (self.mass * self.length**2)

for s in iterate_step(lambda s: leap_frog(0.05, IdealPendulum(1.0, 1.0), s), halt_at_time(100.0), State(0.0, 0.1, 0.0)):
    print(s.time, s.position, s.momentum)
```

# Question time

## Thanks
- Documentation:
    - [mypy-lang.org](https://mypy-lang.org/)
- If you particularly like this approach:
    - [haskell.org](https://haskell.org/)
- If you still can't get enough:
    - [Milewski - Catagory Theory for Programmers](https://github.com/hmemcpy/milewski-ctfp-pdf/)
    - and lectures on [YouTube](https://www.youtube.com/playlist?list=PLbgaMIhjbmEnaH_LTkxLI7FMa2HsnawM_)

