from abc import abstractmethod
from typing import Any, Callable, Iterable, Optional, Set, Tuple, Union
import math


class StatisticalValue:
    """Statistical Value

    In a stochastic optimization problem, especially in the best arm 
    identification problem, we should maintain the mean, variance, and the 
    number of observations to compute the confidence interval of the values.
    This class stores such values.
    """

    def __init__(self, value: Optional[float] = None):
        self.sum = 0
        self.sum2 = 0
        self.count = 0
        if value:
            self.add(value)

    def add(self, value: Union[float, "StatisticalValue"]):
        """Adds new observation

        Parameters
        ----------
        value
            single observation if it is a `float` and multiple observations if
            it is a `StatisticalValue`.
        """
        if isinstance(value, StatisticalValue):
            self.sum += value.sum
            self.sum2 += value.sum2
            self.count += value.count
        else:
            self.sum += value
            self.sum2 += value**2
            self.count += 1

    @property
    def mean(self) -> float:
        """Returns the population mean of the observations

        The population mean is given by

        .. math:: \\frac{1}{T} \\sum_{i=1}^T X_i

        where :math:`T` is the number of observations and :math:`X_i` is the :math:`i`-th observation.

        """
        return self.sum / self.count

    @property
    def var(self) -> float:
        """Returns the population variance of the observations

        The population variance is given by

        .. math:: \\frac{T}{T - 1} \\left[ \\frac{1}{T} \\sum_{i=1}^T X_i^2 - \\left( \\frac{1}{T} \\sum_{i=1}^T X_i \\right) \\right]

        where :math:`T` is the number of observations and :math:`X_i` is the :math:`i`-th observation.

        """
        return (self.sum2/self.count - self.mean**2) * self.count/(self.count - 1)

    def radius(self, a: float, b: float) -> float:
        """Returns the radius of the confidence interval

        In the multi-armed bandit, the radius of the confidence interval is given by the formula 

        .. math:: \\beta(T; a, b) = \\sqrt{\\frac{2 a \sigma^2}{T}} + \\frac{(7/3) a b}{T - 1}

        where :math:`a` and :math:`b` are parameters and :math:`T` is the number of observations of the arm.
        """
        return math.sqrt(2*a*self.var/self.count) + (7/3)*a*b/(self.count - 1)

    def ucb(self, a: float, b: float) -> float:
        """Returns the upper confidence bound

        The upper confidence bound is given by :math:`\\mu + \\beta(T, a, b)` 
        where :math:`\\mu` is the average and :math:`\\beta` is the radius
        of the confidence interval.
        """
        if self.count == 0:
            return math.inf
        return self.mean + self.radius(a, b)

    def lcb(self, a: float, b: float) -> float:
        """Returns the lower confidence bound

        The lower confidence bound is given by :math:`\\mu - \\beta(T, a, b)` 
        where :math:`\\mu` is the average and :math:`\\beta` is the radius
        of the confidence interval.
        """
        if self.count == 0:
            return -math.inf
        return self.mean - self.radius(a, b)

    def __repr__(self):
        return f"Record(mean={self.mean}, var={self.var}, count={self.count})"


class Optimizer:
    def __init__(self, *,
                 maximize: bool = True,
                 budget: Optional[int] = None,
                 confidence: Optional[float] = None):
        """The constructor of the abstract statistical optimizer class

        Parameters
        ----------
        maximize
            True if we want to maximize
        support
            support of the objective function, i.e., fn: 2^{support} -> float.
        cardinality
            size of the solution to be found.
        """
        self.maximize = maximize
        self.budget = budget
        self.confidence = confidence

    def optimal_solution(self) -> Any:
        """Returns an optimal solution

        This method calls `best_arm()` method and drops the objective value.
        """
        S, _ = self.optimize()
        return S

    @abstractmethod
    def optimize(self) -> Tuple[Any, StatisticalValue]:
        """Returns an optimal solution and the objective value

        Each optimizers must implement this method.
        """
        raise NotImplementedError


class CombinatorialOptimizer(Optimizer):
    def __init__(self,
                 fn: Callable[[Set[Any]], float],
                 support: Iterable[Any],
                 cardinality: int,
                 *,
                 maximize: bool = True,
                 budget: Optional[int] = None,
                 confidence: Optional[float] = None,
                 ):
        """The constructor of the abstract optimizer class

        An optimizer regards each combination of the elements as an arm and 
        applies the best arm identification algorithm. So, in the optimizer 
        context, we use words "arm" and "solution" interchangeably.

        Parameters
        ----------
        fn
            objective fucntion.
        support
            support of the objective function, i.e., fn: 2^{support} -> float.
        cardinality
            size of the solution to be found.
        """
        super().__init__(maximize=maximize, budget=budget, confidence=confidence)
        self.fn = fn
        self.support = support
        self.cardinality = cardinality
