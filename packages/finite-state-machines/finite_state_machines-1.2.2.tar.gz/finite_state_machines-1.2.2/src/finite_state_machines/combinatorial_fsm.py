from collections import defaultdict
from typing import (
    IO,
    DefaultDict,
    Dict,
    FrozenSet,
    Hashable,
    Iterable,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)

import sympy  # type: ignore
from tqdm import tqdm  # type: ignore

Weight = Union[sympy.polys.polytools.Poly, sympy.Expr]
x = sympy.Symbol("x")


class CombinatorialFSM:
    """
    This class represents a Combinatorial FSM, which is one with no alphabet, just
    directed edges between states that have weights. The weights are sympy polynomials.

    VERY IMPORTANT NOTE: when you add a transition (s1, s2) with weight w, it ADDS that
    weight to any existing transition betweeen that pair, it DOES NOT OVERWRITE.
    """

    def __init__(self, main_var: Optional[sympy.Symbol] = None) -> None:
        self.start: Optional[Hashable] = None
        self.accepting: Optional[Set[Hashable]] = None
        self.states: Set[Hashable] = set()
        self.transition_weights: DefaultDict[
            Tuple[Hashable, Hashable], Weight
        ] = defaultdict(lambda: sympy.sympify(0))
        self.forward_transitions: DefaultDict[Hashable, Set[Hashable]] = defaultdict(
            set
        )
        # self.backward_transitions: DefaultDict[Hashable, Set[Hashable]] = defaultdict(
        #     set
        # )
        self.main_var: sympy.Symbol = x if main_var is None else main_var
        self.max_degree: int = 0

    def set_start(self, start: Hashable) -> None:
        """sets the start state"""
        self.start = start

    def set_accepting(self, accepting: Iterable[Hashable]) -> None:
        """sets the set of accept states"""
        self.accepting = set(accepting)

    def add_transition(
        self, state1: Hashable, state2: Hashable, weight: Weight
    ) -> None:
        """
        Adds a new edge to the FSM by ***ADDING*** the given weight to any existing
        weight between these two states.
        """
        self.states.update({state1, state2})
        weight_poly = weight.as_poly(self.main_var)
        assert (
            weight_poly.coeff_monomial(1) == 0
        ), "weights must have a zero constant term"
        self.max_degree = max(self.max_degree, weight_poly.degree(self.main_var))

        self.transition_weights[(state1, state2)] += weight_poly
        # self.transition_weights[(state1, state2)] = self.transition_weights[
        #     (state1, state2)
        # ]
        self.forward_transitions[state1].add(state2)
        # self.backward_transitions[state2].add(state1)

    def enumeration(self, size: int, quiet: bool = True) -> List[int]:
        """
        Returns the counting sequence of accepted words up to a given size using
        dynamic programming.
        """
        assert (
            self.start is not None and self.accepting is not None
        ), "start and accepting states must be set"
        enum: List[Weight] = [sympy.sympify(1 if self.start in self.accepting else 0)]

        counts: List[DefaultDict[Hashable, Weight]] = [
            defaultdict(lambda: sympy.sympify(0)) for j in range(self.max_degree + 1)
        ]
        counts[-1][self.start] = sympy.sympify(1)

        loop = range(size) if quiet else tqdm(range(size))
        for _ in loop:

            # had to do this in two steps to make mypy happy
            new_dict: DefaultDict[Hashable, Weight] = defaultdict(
                lambda: sympy.sympify(0)
            )
            counts = counts[1:] + [new_dict]

            for look_back in range(1, self.max_degree + 1):
                for old_state in self.forward_transitions:
                    for new_state in self.forward_transitions[old_state]:
                        transition_weight = self.transition_weights[
                            (old_state, new_state)
                        ]
                        counts[-1][new_state] += (
                            transition_weight.coeff_monomial(self.main_var ** look_back)
                            * counts[-1 - look_back][old_state]
                        )

            enum.append(
                sum(  # type: ignore
                    counts[-1][state] for state in self.accepting
                ).expand()
            )

        return enum

    def minimize(self) -> "CombinatorialFSM":
        """
        Minimization routine. Returns a new CombinatorialFSM object.
        """
        # Minimization Algorithm:
        #  Two states S1 and S2 can be merged if their out-arrows are the same
        #    (i.e., their rows in the transition matrix are equal)
        #  To merge them, pick a representative, say S1. Any state going to S1 or S2 now
        #    goes to S1 (adding such weight, so T -> S1 and T -> S2 don't overwrite each
        #    other).
        #  Out arrows from the new merges state stay the same, not additive.
        #  So, we first group all states into equivalence nodes based on equality of
        #    their out arrows. Suppose A_i is the representative of eq. class E_i. Then
        #    the new transition weights are (E_i -> E_j) = sum(A_i -> B, B in E_j).

        # first we pass through the transition_weights dict to gather the out-arrows per
        #  state, and we include whether or not the state is accepting as well
        Signature = Tuple[bool, Set[Tuple[Hashable, Weight]]]
        HashableSignature = Tuple[bool, FrozenSet[Tuple[Hashable, Weight]]]
        out_weights: Dict[Hashable, Signature] = dict()
        for (state1, state2), weight in self.transition_weights.items():
            if state1 not in out_weights:
                out_weights[state1] = (state1 in self.accepting, set())
            out_weights[state1][1].add((state2, weight))

        # now group states into equivalence classes based on out_weights, essentially
        #   just reversing out_weights
        eq_class_dict: DefaultDict[HashableSignature, Set[Hashable]] = defaultdict(set)
        unassigned_states = set(self.states)
        for state, sig in out_weights.items():
            eq_class_dict[(sig[0], frozenset(sig[1]))].add(state)
            unassigned_states.remove(state)
        # also need to add an eq class for states that have no out-transitions
        for un_state in unassigned_states:
            eq_class_dict[(un_state in self.accepting, frozenset())].add(un_state)

        # the values of eq_class_dict are now the equivalence classes
        # we now want a dictionary to convert any state into the representative of its
        #  eq_class as well as a dictionary that maps a rep to the eq_class
        representative: Dict[Hashable, Hashable] = dict()
        rep_to_eq_class: DefaultDict[Hashable, Set[Hashable]] = defaultdict(set)
        for eq_class in eq_class_dict.values():
            rep = min(eq_class)  # type: ignore
            for state in eq_class:
                representative[state] = rep
                rep_to_eq_class[rep].add(state)
        rep_set = set(representative.values())

        newCFSM = CombinatorialFSM(self.main_var)
        # set start and accepting
        newCFSM.set_start(representative[self.start])
        newCFSM.set_accepting({representative[acc] for acc in self.accepting})

        for state1 in rep_set:
            for state2 in rep_set:
                new_weight = sum(
                    self.transition_weights[(state1, dest)]
                    for dest in rep_to_eq_class[state2]
                    if (state1, dest) in self.transition_weights
                )
                if new_weight != 0:
                    newCFSM.add_transition(state1, state2, new_weight)

        return newCFSM

    def write_to_maple_file(self, file: IO) -> None:
        """
        Writes a maple file to <file> that creates the matrix and solves for the GF.
        """

        # First we need a state -> int mapping, and it has to be 1 based, because
        #  Maple is
        state_to_int: Dict[Hashable, int] = dict()
        counter = 1
        for state in self.states:
            state_to_int[state] = counter
            counter += 1

        num_states = len(self.states)
        print(f"start := {state_to_int[self.start]}:", file=file)
        print(f"accepting := {[state_to_int[a] for a in self.accepting]}:", file=file)
        print(f"M := Matrix({num_states},{num_states}, storage=sparse):", file=file)

        for (state1, state2), weight in self.transition_weights.items():
            print(
                f"M[{state_to_int[state1]},{state_to_int[state2]}] := "
                f"{(weight*-1).as_expr()}:",
                file=file,
            )
        for index in range(1, num_states + 1):
            print(f"M[{index},{index}] := 1 + M[{index},{index}]:", file=file)

        print("V := Vector(LinearAlgebra[Dimensions](M)[1]):", file=file)
        print("for a in accepting do V[a] := 1: od:", file=file)
        print("infolevel[solve] := 5:", file=file)
        print("xvec := LinearAlgebra[LinearSolve](M, V):", file=file)
        print(f"f := xvec[{state_to_int[self.start]}]:", file=file)
