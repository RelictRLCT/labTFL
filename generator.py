from typing import Mapping, Any, AbstractSet

from automata.fa.dfa import DFA
from automata.fa.nfa import NFA
from show import show
# Буду строить НКА с помощью случайной регулярки, потом перевод в ДКА и минимизация
# Длина регулярки должна быть примерно log(N) по основанию 2, где N - оценка сверху числа состояний (худший случай -
# экспоненциальный рост при переводе НКА в ДКА (перевод регулярки в НКА примерно O(n) от длины регулярки)
def generate_regex() -> str:
    return 'L|RL*L|RRLR|R*L*R|RRRL+R*LR|LLL'


# Функция для удаления финальных состояний, которые не являются тупиковыми
def remove_not_dead_end(finals: AbstractSet, transitions: Mapping[Any, Mapping[str, Any]]) -> AbstractSet:
    new_finals = set()
    for fin in finals:
        for fin2 in transitions[fin].values():
            if fin2 != fin:
                break
        else:
            new_finals.add(fin)
    return new_finals


def generate_labyrinth() -> DFA:
    init_dfa = DFA(
        states={'q0'},
        input_symbols={'1'},
        transitions={'q0': {'1': 'q0'}},
        initial_state='q0',
        final_states={'q0'}
    )

    init_nfa = NFA(
        states={'q0'},
        input_symbols={'1'},
        transitions={'q0': {'1': {'q0'}}},
        initial_state='q0',
        final_states={'q0'}
    )

    # Генерация регулярки и НКА по ней
    regex = generate_regex()
    init_nfa = init_nfa.from_regex(regex=regex, input_symbols={'L', 'R'})

    # Детерминизация
    init_dfa = init_dfa.from_nfa(target_nfa=init_nfa)

    show(init_dfa)

    # Избавление от нетупиковых финальных состояний, которые могли появиться
    new_final_states = remove_not_dead_end(init_dfa.final_states, init_dfa.transitions)

    # Создание итогового лабиринта
    labyrinth = DFA(
        states=init_dfa.states,
        input_symbols=init_dfa.input_symbols,
        transitions=init_dfa.transitions,
        initial_state=init_dfa.initial_state,
        final_states=new_final_states,
        allow_partial=True
    )

    return labyrinth
