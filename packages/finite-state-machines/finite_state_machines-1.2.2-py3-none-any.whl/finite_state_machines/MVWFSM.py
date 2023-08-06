"""
This module provides the MultivariateWeightedFiniteStateMachine class.

HIGHLY EXPERIMENTAL! MANY FUNCTIONS HAVE NOT BEEN EXTENSIVELY TESTED.
"""
from typing import Dict, List, Set, Tuple, Union

import sympy  # type: ignore
from tqdm import tqdm  # type: ignore


class MultivariateWeightedFiniteStateMachine:  # pylint: disable=R0902
    """
    alphabet: set of length 1 strings
    num_states: integer
    start: integer
    accepting: set of integers
    weighted_transitions: dictionary, (integer, string): (integer, weight)
            where "weight" is a sympy polynomial in the main variable "x" and other
            variables y
    """

    def __init__(
        self,
        alphabet: Set[str],
        num_states: int,
        start: int,
        accepting: Set[int],
        weighted_transitions: Dict[
            Tuple[int, str], Tuple[int, Union[sympy.polys.polytools.Poly, sympy.Expr]]
        ],
        weight_vars: Set[sympy.core.symbol.Symbol],
    ):
        self.alphabet = alphabet
        self.num_states = num_states
        self.start = start
        self.accepting = accepting

        self.max_degree = 0
        self.x = sympy.symbols("x")
        self.weighted_transitions = dict()

        for ((state, letter), (next_state, weight)) in weighted_transitions.items():
            assert isinstance(
                weight, (sympy.Expr, sympy.polys.polytools.Poly)
            ), "weight must be a Sympy polynomial"
            weight_poly = weight.as_poly(list(weight_vars))
            # assert (
            #     self.x in weight_poly.free_symbols
            # ), "weights must at least be in the sympy variable 'x'"]
            assert (
                weight_poly.coeff_monomial(1) == 0
            ), "weights must have a zero constant term"
            self.max_degree = max(self.max_degree, weight_poly.degree(self.x))
            self.weighted_transitions[(state, letter)] = (next_state, weight_poly)

        # keys are the size of words (by weight, not length!)
        # values are dicts whose
        #   keys represent which states they end in
        #   values are the sets of words of that size that end in that state
        self._word_cache: Dict[int, Dict[int, Set[str]]] = dict()

        # It is assumed that there is no implicit garbage state if all possible
        # transitions are present.
        if self.num_states * len(self.alphabet) == len(
            self.weighted_transitions.keys()
        ):
            self.explicit_garbage = True
        else:
            self.explicit_garbage = False

    def add_explicit_garbage(self) -> None:
        """
        Adds an explicit garbage state rather than relying on an implicit one.
        This is necessary for the minimize function to operate correctly.
        """
        if self.explicit_garbage:
            return
        garbage_state = self.num_states
        self.num_states += 1
        for state in range(self.num_states - 1):
            for letter in self.alphabet:
                if (state, letter) not in self.weighted_transitions:
                    self.weighted_transitions[(state, letter)] = (garbage_state, self.x)
        for letter in self.alphabet:
            self.weighted_transitions[(garbage_state, letter)] = (garbage_state, self.x)
        self.explicit_garbage = True

    def smart_enumeration(
        self, size: int, quiet: bool = False, special_simplify: bool = False
    ) -> List[sympy.polys.polytools.Poly]:
        """
        Returns the counting sequence of accepted words up to a given size using
        dynamic programming.
        """
        enum = [1 if self.start in self.accepting else 0]
        y = sympy.symbols("y")
        counts = [
            [0 for i in range(self.num_states)] for j in range(self.max_degree + 1)
        ]
        counts[-1][self.start] = 1

        loop = range(size) if quiet else tqdm(range(size))
        for val in loop:
            counts = counts[1:] + [[0 for i in range(self.num_states)]]

            for look_back in range(1, self.max_degree + 1):
                for (
                    (old_state, _),
                    (new_state, weight),
                ) in self.weighted_transitions.items():
                    counts[-1][new_state] += (
                        weight.as_expr().coeff(self.x ** look_back)
                        * counts[-1 - look_back][old_state]
                    )
                    # if (
                    #     special_simplify
                    #     and type(sympy.collect(counts[-1][new_state], y)).func
                    #     == sympy.core.add.Add
                    # ):
                    #     counts[-1][new_state] = sum(
                    #         term.expand()
                    #         for term in sympy.collect(counts[-1][new_state], y).args
                    #     )
                    # else:
                    # counts[-1][new_state] = counts[-1][new_state].expand()
            to_append = sum(
                [counts[-1][i] for i in range(self.num_states) if i in self.accepting]
            )
            if (
                special_simplify
                and type(sympy.collect(to_append, y)) == sympy.core.add.Add
            ):
                to_append = sum(
                    term.expand() for term in sympy.collect(to_append, y).args
                )
            else:
                to_append = to_append.expand()
            enum.append(to_append)

        return enum
