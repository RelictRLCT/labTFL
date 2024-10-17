from automata.fa.dfa import DFA
from automata.fa.nfa import NFA
from show import show

if __name__ == "__main__":
    dfa1 = DFA(
        states={'q0', 'q1', 'q2'},
        input_symbols={'1'},
        transitions={
            'q0': {'1': 'q1'},
            'q1': {'1': 'q2'},
            'q2': {'1': 'q2'}
        },
        initial_state='q0',
        final_states={'q2'},
        allow_partial=True
    )

    # dfa2 = DFA(
    #     states={'q3', 'q4', 'q5'},
    #     input_symbols={'1'},
    #     transitions={
    #         'q3': {'1': 'q4'},
    #         'q4': {'1': 'q5'},
    #         'q5': {}
    #     },
    #     initial_state='q3',
    #     final_states={'q3'},
    #     allow_partial=True
    # )

    dfa2 = DFA(
        states={'q0', 'q1', 'q2'},
        input_symbols={'1'},
        transitions={
            'q0': {'1': 'q1'},
            'q1': {'1': 'q2'},
            'q2': {'1': 'q2'}
        },
        initial_state='q0',
        final_states={'q2'},
        allow_partial=True
    )

    show(dfa1)
    show(dfa2)
    dfa1 = dfa1.symmetric_difference(dfa2)
    show(dfa1)
    # Надо будет взять симметрическую разность двух автоматов, и, если язык полученного автомата пустой,
    # то автоматы эквивалентны. Иначе вернуть случайное слово из автомата симметрической разности