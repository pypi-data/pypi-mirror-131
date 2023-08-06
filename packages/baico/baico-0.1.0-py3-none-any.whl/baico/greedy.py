from typing import Any, Tuple
from . import BestArmIdentification
from .base import StatisticalValue, CombinatorialOptimizer


class Greedy(CombinatorialOptimizer):
    def optimize(self) -> Tuple[Any, StatisticalValue]:
        S = frozenset()
        value = StatisticalValue()
        for _ in range(self.cardinality):
            bai = BestArmIdentification(
                fn=self.fn,
                arms=[S.union([e]) for e in self.support if e not in S],
                budget=self.budget,
                confidence=self.confidence
            )
            S, value = bai.optimize()
        return S, value
