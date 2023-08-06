from typing import Any, Callable, Iterable, Optional, Set
from .base import Optimizer
from .best_arm_identification import ArmData, BestArmIdentification


class IncrementalBeamSearch(Optimizer):
    def __init__(self,
                 fn: Callable[[Set[Any]], float],
                 support: Iterable[Any],
                 cardinality: int,
                 *,
                 maximize: bool = True,
                 budget: Optional[int] = None,
                 confidence: Optional[float] = None,
                 ):
        super().__init__(fn, support, cardinality, maximize=maximize, budget=budget, confidence=confidence)
        self.records = {}
        self.open = [set() for _ in range(cardinality+1)]
        self.close = [set() for _ in range(cardinality+1)]

    def create_record(self, x):
        if x in self.records:
            return
        k = len(x)
        self.open[k].add(x)
        self.records[x] = ArmData()
        self.records[x].add(self.fn(x))
        self.records[x].add(self.fn(x))

    def init(self):
        self.create_record(frozenset())

    def step(self, num_repeats):
        for _ in range(num_repeats):
            for k in range(self.cardinality):
                arms = {
                    x: self.records[x] for x in self.open[k]
                }
                bai = BestArmIdentification(
                    fn=self.fn,
                    arms=arms,
                    budget=self.budget or 100*len(arms),
                    confidence=self.confidence or 0.1
                )
                x = bai.run()
                if x is not None:
                    self.open[k].remove(x)
                    self.close[k].add(x)
                    for e in self.support:
                        if e not in x:
                            self.create_record(x.union(frozenset([e])))

    def best_solution(self, cardinality=None):
        k = cardinality or self.cardinality
        arms = {
            x: self.records[x] for x in self.open[k].union(self.close[k])
        }
        bai = BestArmIdentification(
            fn=self.fn,
            arms=arms,
            budget=self.budget or 100*len(arms),
            confidence=self.confidence or 0.1
        )
        return bai.run()

    def run(self, num_repeats=2):
        self.init()
        self.step(num_repeats)
        return self.best_solution()
