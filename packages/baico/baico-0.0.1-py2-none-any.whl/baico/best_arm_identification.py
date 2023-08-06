from typing import Any, Dict, Iterable, Optional, Union
import math


class ArmData:
    def __init__(self):
        self.sum = 0
        self.sum2 = 0
        self.count = 0

    def add(self, value: float):
        self.sum += value
        self.sum2 += value*value
        self.count += 1

    @property
    def mean(self) -> float:
        return self.sum / self.count

    @property
    def var(self) -> float:
        return (self.sum2/self.count - self.mean**2) * self.count/(self.count - 1)

    def radius(self, a, b) -> float:
        return math.sqrt(2*a*self.var/self.count) + (7/3)*a*b/(self.count - 1)

    def ucb(self, a, b) -> float:
        if self.count == 0:
            return math.inf
        return self.mean + self.radius(a, b)

    def lcb(self, a, b) -> float:
        if self.count == 0:
            return -math.inf
        return self.mean - self.radius(a, b)

    def __repr__(self):
        return f"Record(mean={self.mean}, var={self.var}, count={self.count})"


class BestArmIdentification:
    """
    Variance-Based Best Arm Identification

    https://hal.inria.fr/hal-00747005v1/document
    """

    def __init__(self, *,
                 fn,
                 arms: Union[Iterable[Any], Dict[Any, ArmData]],
                 budget: Optional[int] = None,
                 confidence: Optional[float] = None,
                 maximize: bool = True):

        self.fn = fn if maximize else lambda x: -fn(x)
        if isinstance(arms, Dict):
            self.arms = arms
        else:
            self.arms = {}
            for x in arms:
                arm = ArmData()
                arm.add(self.fn(x))
                arm.add(self.fn(x))
                self.arms[x] = arm

        self.budget = budget
        self.confidence = confidence
        if confidence is not None:
            self.a = lambda t: math.log(
                4 * len(self.arms) * t**3 / confidence) / 2
        else:
            assert budget is not None
            self.a = lambda t: self.budget / len(arms)

        self.b = 1.0
        self.t = sum(arm.count for arm in self.arms.values())
        self.maximize = True

    def run(self) -> Optional[Any]:
        if len(self.arms) <= 1:
            x = None
            for y in self.arms.keys():
                x = y
            return x

        while True:
            # Select two largest elements by UCB
            x1, ucb1 = None, None
            x2, ucb2 = None, None
            for x, arm in self.arms.items():
                ucb = arm.ucb(self.a(self.t), self.b)
                if ucb1 is None or ucb > ucb1:
                    x2, ucb2 = x1, ucb1
                    x1, ucb1 = x, ucb
                elif ucb2 is None or ucb > ucb2:
                    x2, ucb2 = x, ucb

            # Select the candidate of optimal solution
            y, gap = None, None
            for x, arm in self.arms.items():
                lcb = arm.lcb(self.a(self.t), self.b)
                if x == x1:
                    score = ucb2 - lcb
                else:
                    score = ucb1 - lcb
                if gap is None or score < gap:
                    y, gap = x, score

            if y == x1:
                z = x2
            else:
                z = x1

            if self.arms[y].count < self.arms[z].count:
                self.arms[y].add(self.fn(y))
            else:
                self.arms[z].add(self.fn(z))
            self.t += 1

            if self.budget and self.t >= self.budget:
                break
            if self.confidence and gap < self.confidence:
                break

        return y
