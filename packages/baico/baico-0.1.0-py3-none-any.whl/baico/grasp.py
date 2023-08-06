from typing import Any, Callable, Iterable, Optional, Set, Tuple
import random
from . import BestArmIdentification, StochasticGreedy
from .base import CombinatorialOptimizer, StatisticalValue


class GreedyRandomizedAdaptiveSearchProcedure(CombinatorialOptimizer):
    """Creates a Greedy Randomized Adaptive Search Procedure (GRASP) optimizer

    GRASP is a off-the-shelf optimization metaheuristics for combinatorial 
    optimization problems.  It iteratively finds a initial solution by a 
    randomised version of greedy algorithm. Then it improves the solution by 
    the local search. See 
    https://en.wikipedia.org/wiki/Greedy_randomized_adaptive_search_procedure 
    for the detail.

    Parameters
    ----------
    `num_repeats`
        The number of initial solutions. 

    `num_local_search`
        number of local searth paths. 
    """

    def __init__(self,
                 fn: Callable[[Set[Any]], float],
                 support: Iterable[Any],
                 cardinality: int,
                 *,
                 maximize: bool = True,
                 budget: Optional[int] = None,
                 confidence: Optional[float] = None,
                 num_repeats=2,
                 num_local_search=5,
                 ):
        super().__init__(fn,
                         support,
                         cardinality,
                         maximize=maximize,
                         budget=budget,
                         confidence=confidence)
        self.num_repeats = num_repeats
        self.num_local_search = num_local_search

    def optimize(self) -> Tuple[Any, StatisticalValue]:
        """Returns the best solution with ArmData.
        """
        optimal_arms = {}
        for _ in range(self.num_repeats):
            # construct a solution by oversampling
            construct = StochasticGreedy(self.fn, self.support,
                                         cardinality=self.cardinality,
                                         maximize=self.maximize,
                                         budget=self.budget,
                                         confidence=self.confidence)
            S, arm = construct.optimize()

            for _ in range(self.num_local_search):
                updated = False
                inner = list(S)
                random.shuffle(inner)
                for a in inner:
                    for b in self.support:
                        if a not in S:
                            break
                        if b in S:
                            continue
                        T = S.symmetric_difference(frozenset([a, b]))
                        arms = {
                            S: arm,
                            T: StatisticalValue()
                        }
                        bai = BestArmIdentification(fn=self.fn,
                                                    arms=arms,
                                                    budget=self.budget,
                                                    confidence=self.confidence)
                        S, arm = bai.optimize()
                        if b in S:
                            updated = True
                if not updated:
                    break
            if S not in optimal_arms:
                optimal_arms[S] = StatisticalValue()
            optimal_arms[S].add(arm)

        bai = BestArmIdentification(fn=self.fn,
                                    arms=optimal_arms,
                                    budget=self.budget,
                                    confidence=self.confidence)
        return bai.optimize()
