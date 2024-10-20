from automata.fa.dfa import DFA
from show import show
from dfa_from_table import make_dfa_from_table


def equal_labyrinths(labyrinth: DFA, learner_dfa: DFA | str) -> str:
    if learner_dfa is str:
        learner_dfa = make_dfa_from_table(learner_dfa)

    dfa = labyrinth.symmetric_difference(learner_dfa)

    if dfa.isempty():
        return 'true'
    else:
        k = 0
        while True:
            try:
                return dfa.random_word(k)
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

    # Надо будет взять симметрическую разность двух автоматов, и, если язык полученного автомата пустой,
    # то автоматы эквивалентны. Иначе вернуть случайное слово из автомата симметрической разности