# ~\~ language=Python filename=examples/integrator.py
# ~\~ begin <<README.md|examples/integrator.py>>[0]
from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, TypeVar, Callable, Iterable, Generic
import numpy as np

Vector = TypeVar("Vector", bound="VectorProtocol")

class VectorProtocol(Protocol):
    def __add__(self: Vector, other: Vector) -> Vector: ...
    def __rmul__(self: Vector, other: float) -> Vector: ...

class HamiltonianSystem(Protocol[Vector]):
    def momentumEquation(self, s: State[Vector]) -> Vector: ...
    def positionEquation(self, s: State[Vector]) -> Vector: ...

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
# ~\~ end
