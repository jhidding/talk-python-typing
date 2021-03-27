# ~\~ language=Python filename=examples/generic.py
# ~\~ begin <<README.md|examples/generic.py>>[0]
from typing import (Iterable)

def word_lengths(words: Iterable[str]) -> Iterable[int]:
    return (len(w) for w in words)

words = "The quick brown fox jumps over the lazy dog".split()
print(word_lengths(words))
print(word_lengths(w.upper() for w in words))
# ~\~ end
