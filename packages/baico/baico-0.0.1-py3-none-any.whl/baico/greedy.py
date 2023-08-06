from .base import Optimizer
from .best_arm_identification import BestArmIdentification


class Greedy(Optimizer):
    def run(self):
        S = frozenset()
        for _ in range(self.cardinality):
            arms = [S.union([e]) for e in self.support if e not in S]
            bai = BestArmIdentification(
                fn=self.fn,
                arms=arms,
                budget=self.budget or 100*len(arms),
                confidence=self.confidence or 0.1
            )
            S = bai.run()
        return S
