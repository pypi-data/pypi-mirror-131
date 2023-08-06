from typing import Any, Callable, Iterable, Optional, Set
import random
import math
from .base import Optimizer
from .best_arm_identification import BestArmIdentification


class StochasticGreedy(Optimizer):
    def __init__(self,
                 fn: Callable[[Set[Any]], float],
                 support: Iterable[Any],
                 cardinality: int,
                 *,
                 maximize: bool = True,
                 budget: Optional[int] = None,
                 confidence: Optional[float] = None,
                 epsilon: float = 0.2
                 ):
        super().__init__(fn, support, cardinality, maximize=maximize, budget=budget, confidence=confidence)
        self.epsilon = epsilon

    def run(self):
        S = frozenset()
        size = (int)(len(self.support) / self.cardinality * math.log(1.0 / self.epsilon))
        for _ in range(self.cardinality):
            candidates = [S.union([e]) for e in self.support if e not in S]
            if size >= len(candidates):
                arms = candidates
            else:
                arms = random.sample(candidates, size)
            bai = BestArmIdentification(
                fn=self.fn,
                arms=arms,
                budget=self.budget or 100*len(arms),
                confidence=self.confidence or 0.1
            )
            S = bai.run()
        return S
