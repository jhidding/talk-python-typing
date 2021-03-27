# ~\~ language=Python filename=examples/tree.py
# ~\~ begin <<README.md|examples/tree.py>>[0]
from dataclasses import dataclass
from typing import (TypeVar, Generic, Optional, Union)

T = TypeVar("T")

@dataclass
class Tree(Generic[T]):
    value: T
    left: Optional[Tree[T]] = None
    right: Optional[Tree[T]] = None

x = Tree(1, left=Tree(2, right=Tree(3)), right=Tree(4))
# y = Tree(1, left=Tree(2, right=Tree(3)), right=Tree("hello"))
y: Tree[Union[int, str]] \
    = Tree(1, left=Tree(2, right=Tree(3)), right=Tree("hello"))
# ~\~ end
