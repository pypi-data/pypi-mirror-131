from abc import abstractmethod
from typing import Any, Callable, Iterable, Optional, Set


class Optimizer:
    def __init__(self,
                 fn: Callable[[Set[Any]], float],
                 support: Iterable[Any],
                 cardinality: int,
                 *,
                 maximize: bool = True,
                 budget: Optional[int] = None,
                 confidence: Optional[float] = None,
                 ):
        self.fn = fn
        self.support = support
        self.cardinality = cardinality
        self.maximize = maximize
        self.budget = budget
        self.confidence = confidence

    @abstractmethod
    def run(self):
        pass
