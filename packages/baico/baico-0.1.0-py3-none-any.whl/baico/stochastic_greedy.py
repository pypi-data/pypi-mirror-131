from typing import Any, Callable, Iterable, Optional, Set, Tuple
import random
import math
from . import BestArmIdentification
from .base import StatisticalValue, CombinatorialOptimizer


class StochasticGreedy(CombinatorialOptimizer):
    """
    Stochastic Greedy Algorithm
    """
    def __init__(self,
                 fn: Callable[[Set[Any]], float],
                 support: Iterable[Any],
                 cardinality: int,
                 *,
                 maximize: bool = True,
                 budget: Optional[int] = None,
                 confidence: Optional[float] = None,
                 epsilon: float = 0.2,
                 num_repeats: int = 1):
        super().__init__(fn,
                         support,
                         cardinality,
                         maximize=maximize,
                         budget=budget,
                         confidence=confidence)
        self.num_repeats = num_repeats
        self.epsilon = epsilon

    def optimize(self) -> Tuple[Any, StatisticalValue]:
        optimal_arms = {}
        for _ in range(self.num_repeats):
            S = frozenset()
            value = StatisticalValue()
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
                    budget=self.budget,
                    confidence=self.confidence
                )
                S, value = bai.optimize()

            if S not in optimal_arms:
                optimal_arms[S] = StatisticalValue()
            optimal_arms[S].add(value)

        bai = BestArmIdentification(
            fn=self.fn,
            arms=optimal_arms,
            budget=self.budget,
            confidence=self.confidence
        )
        return bai.optimize()
