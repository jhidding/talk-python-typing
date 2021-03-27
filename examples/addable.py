# ~\~ language=Python filename=examples/addable.py
# ~\~ begin <<README.md|examples/addable.py>>[0]
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
# ~\~ end
