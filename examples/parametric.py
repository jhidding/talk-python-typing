# ~\~ language=Python filename=examples/parametric.py
# ~\~ begin <<README.md|examples/parametric.py>>[0]
def word_lengths(words: list[str]) -> list[int]:
    return [len(w) for w in words]

words = "The quick brown fox jumps over the lazy dog".split()
print(word_lengths(words))
print(word_lengths(w.upper() for w in words))
# ~\~ end
