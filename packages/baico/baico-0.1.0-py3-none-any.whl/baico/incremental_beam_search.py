from typing import Any, Callable, Iterable, Optional, Set, Tuple
from . import BestArmIdentification
from .base import StatisticalValue, CombinatorialOptimizer


class IncrementalBeamSearch(CombinatorialOptimizer):
    def __init__(self,
                 fn: Callable[[Set[Any]], float],
                 support: Iterable[Any],
                 cardinality: int,
                 *,
                 maximize: bool = True,
                 budget: Optional[int] = None,
                 confidence: Optional[float] = None,
                 ):
        super().__init__(fn,
                         support,
                         cardinality,
                         maximize=maximize,
                         budget=budget,
                         confidence=confidence)
        self.records = {}
        self.open = [set() for _ in range(cardinality+1)]
        self.close = [set() for _ in range(cardinality+1)]

    def _create_record(self, x):
        if x in self.records:
            return
        k = len(x)
        self.open[k].add(x)
        self.records[x] = StatisticalValue()

    def _init(self):
        self._create_record(frozenset())

    def _step(self, num_repeats: int):
        for _ in range(num_repeats):
            for k in range(self.cardinality):
                if len(self.open[k]) == 0:
                    continue
                arms = {
                    x: self.records[x] for x in self.open[k]
                }
                bai = BestArmIdentification(
                    fn=self.fn,
                    arms=arms,
                    budget=self.budget,
                    confidence=self.confidence
                )
                x = bai.optimal_solution()
                if x is not None:
                    self.open[k].remove(x)
                    self.close[k].add(x)
                    for e in self.support:
                        if e not in x:
                            self._create_record(x.union(frozenset([e])))

    def _best_solution(self,
                      cardinality: Optional[int] = None
                      ) -> Tuple[Any, StatisticalValue]:
        k = cardinality or self.cardinality
        bai = BestArmIdentification(
            fn=self.fn,
            arms={
                x: self.records[x] for x in self.open[k].union(self.close[k])
            },
            budget=self.budget,
            confidence=self.confidence
        )
        return bai.optimize()

    def optimize(self,
                 num_repeats: int = 2) -> Tuple[Any, StatisticalValue]:
        self._init()
        self._step(num_repeats)
        return self._best_solution()
