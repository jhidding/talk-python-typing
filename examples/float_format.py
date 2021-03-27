# ~\~ language=Python filename=examples/float_format.py
# ~\~ begin <<README.md|examples/float_format.py>>[0]
from typing import Callable

FloatFormatter = Callable[[float], str]

my_format: FloatFormatter = "{:.4}".format
# ~\~ end
