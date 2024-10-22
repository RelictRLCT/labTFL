from automata.fa.dfa import DFA
from show import show


def equal_labyrinths(labyrinth: DFA, learner_dfa: DFA) -> (str, bool):

    dfa = labyrinth.symmetric_difference(learner_dfa)

    if dfa.isempty():
        # Эквивалентны
        return None, None
    else:
        dfa = labyrinth.difference(learner_dfa)
        if dfa.isempty():
            k = 0
            while True:
                try:
                    return dfa.random_word(k), False
                except ValueError:
                    k += 1

        k = 0
        while True:
            try:
                return dfa.random_word(k), True
            except ValueError:
                k += 1


def membership(labyrinth: DFA, word: str) -> bool:
    return labyrinth.accepts_input(word)


if __name__ == "__main__":
    dfa1 = DFA(
        states={'e', 'a', 'b', 'ba', 'bb'},
        input_symbols={'a', 'b'},
        transitions={
            'e': {'b': 'b', 'a': 'a'},
            'a': {'a': 'e', 'b': 'ba'},
            'b': {'a': 'ba', 'b': 'bb'},
            'ba': {'a': 'b', 'b': 'bb'},
            'bb': {'a': 'bb', 'b': 'bb'}
        },
        initial_state='e',
        final_states={'b'},
        allow_partial=True
    )

    show(dfa1)

    dfa2 = DFA(
        states={'q1', 'q2', 'trap'},
        input_symbols={'a', 'b'},
        transitions={
            'q1': {'b': 'q2', 'a': 'trap'},
            'trap': {'a': 'trap', 'b': 'trap'},
            'q2': {'a': 'trap', 'b': 'trap'}
        },
        initial_state='q1',
        final_states={'q2'},
        allow_partial=True
    )

    show(dfa2)

    print(equal_labyrinths(dfa1, dfa2))
