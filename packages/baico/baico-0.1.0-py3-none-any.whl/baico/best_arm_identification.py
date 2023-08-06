from typing import Any, Dict, Iterable, Optional, Tuple, Union
import math
from .base import StatisticalValue, Optimizer


class BestArmIdentification(Optimizer):
    def __init__(self, *,
                 fn,
                 arms: Union[Iterable[Any], Dict[Any, StatisticalValue]],
                 maximize: bool = True,
                 budget: Optional[int] = None,
                 confidence: Optional[float] = None,
                 ):
        """Variance-Aware Best Arm Identification solver

        See https://hal.inria.fr/hal-00747005v1/document

        Parameters
        ----------
        fn
            The objective function
        arms
            The set of arms
        maximize
            `True` if we want to find the arm with the largest value
        budget
            The maximum number of evaluations
        confidence
            The target confidence bound
        """

        super().__init__(
            maximize=maximize,
            budget=budget or 100 * len(arms),
            confidence=confidence or 0.1
        )
        self.fn = fn if maximize else lambda x: -fn(x)
        if isinstance(arms, Dict):
            self.arms = arms
        else:
            self.arms = {x: StatisticalValue() for x in arms}
        for x, arm in self.arms.items():
            while arm.count <= 2:
                arm.add(self.fn(x))
        assert len(self.arms) >= 1

        if confidence is not None:
            self.a = lambda t: math.log(
                4 * len(self.arms) * t**3 / confidence) / 2
        else:
            self.a = lambda t: self.budget / len(arms)

        self.b = 1.0
        self.t = sum(arm.count for arm in self.arms.values())

    def optimize(self) -> Tuple[Any, StatisticalValue]:
        if len(self.arms) <= 1:
            for x, arm in self.arms.items():
                return x, arm

        while True:
            # Select two largest elements in UCB
            x1, ucb1 = None, None
            x2, ucb2 = None, None
            for x, arm in self.arms.items():
                ucb = arm.ucb(self.a(self.t), self.b)
                if ucb1 is None or ucb > ucb1:
                    x2, ucb2 = x1, ucb1
                    x1, ucb1 = x, ucb
                elif ucb2 is None or ucb > ucb2:
                    x2, ucb2 = x, ucb

            # Select the first optimal solution candidate
            y, gap = None, None
            for x, arm in self.arms.items():
                lcb = arm.lcb(self.a(self.t), self.b)
                if x == x1:
                    score = ucb2 - lcb
                else:
                    score = ucb1 - lcb
                if gap is None or score < gap:
                    y, gap = x, score

            # Select the second optimal solution candidate
            if y == x1:
                z = x2
            else:
                z = x1

            # Observe data for the less certain arm
            if self.arms[y].count < self.arms[z].count:
                self.arms[y].add(self.fn(y))
            else:
                self.arms[z].add(self.fn(z))
            self.t += 1

            # Stopping rules
            if self.budget and self.t >= self.budget:
                break
            if self.confidence and gap < self.confidence:
                break

        return y, self.arms[y]
