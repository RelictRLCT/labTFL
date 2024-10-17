import random
from itertools import repeat
from pprint import pprint
from typing import Mapping, Any, AbstractSet
import math
from automata.fa.dfa import DFA
from automata.fa.nfa import NFA

from show import show
# Буду строить НКА с помощью случайной регулярки, потом перевод в ДКА и минимизация
# Длина регулярки должна быть примерно log(N) по основанию 2, где N - оценка сверху числа состояний (худший случай -
# экспоненциальный рост при переводе НКА в ДКА (перевод регулярки в НКА примерно O(n) от длины регулярки)
#
# Обновлено: на реальных данных и алфавите из 2 символов зависимость +- линейная, поэтому длину регулярки буду
# использовать равную ограничению из файла, а потом, в случае превышения, удалю случайные состояния
def generate_regex() -> str:
    file = open('parameters.txt', 'r')
    limit = int(file.readline())
    file.close()

    '''Нужна более точная оценка'''
    # limit = limit // 2

    random_count_of_alternate: int
    if limit >= 4:
        random_count_of_alternate = random.randint(a=1, b=limit // 4)
    else:
        random_count_of_alternate = 1

    # Разбиение длины всего выражения на сумму rand_count_of_alternate частей (длИны частей между |)
    pieces = []

    # Сначала заполнил средним значением
    average = limit // random_count_of_alternate
    remainder = limit % random_count_of_alternate
    for i in range (random_count_of_alternate):
        pieces.append(average)
    pieces[random_count_of_alternate - 1] += remainder

    # Генерация случайных флуктуаций
    remainder = 0
    for i in range (random_count_of_alternate):
        fluct = random.randint(0, (limit // random_count_of_alternate) // 2)
        if i // 2 == 0:
            pieces[i] += fluct
            remainder -= fluct
        else:
            pieces[i] -= fluct
            remainder += fluct
    pieces[random_count_of_alternate - 1] += remainder

    regex_alternate_list = []

    # Генерация регулярки
    for len_piece in pieces:
        part_regex = ''
        br_pos = []
        count_of_open_brackets = 0
        for i in range(len_piece):

            # Добавляем скобки (с шансом)
            while not random.randint(-2, 1) in {-2, 0}: # Для шанса добавления нескольких скобок подряд (((
                add_bracket = random.randint(0, 1)
                if i < len_piece - 1: # Нельзя ставить скобку перед предпоследним (иначе в тупике будет цикл)
                    match add_bracket:
                        case 0:
                            pass
                        case 1:
                            br_pos.append(len(part_regex))
                            part_regex += '('
                            count_of_open_brackets += 1

            # Добавляем L или R
            L_or_R = random.randint(0, 1)
            match L_or_R:
                case 0:
                    part_regex += 'L'
                case 1:
                    part_regex += 'R'

            # Добавляем операцию (с шансом)
            operator = random.randint(-1, 3)
            match operator:
                case -1:
                    pass
                case 0:
                    pass
                case 1:
                    part_regex += '*'
                case 2:
                    part_regex += '+'
                case 3:
                    part_regex += '?'

        for i in range(count_of_open_brackets):
            close_pos = random.randint(br_pos[i], len(part_regex) - 2)
            while part_regex[close_pos] == '(' or part_regex[close_pos - 1] == '(':
                close_pos += 1

            # Еще случайная операция после скобки
            oper = ''
            add_symbols_count = 1
            operator = random.randint(-1, 3)
            match operator:
                case -1:
                    pass
                case 0:
                    pass
                case 1:
                    oper = '*'
                    add_symbols_count += 1
                case 2:
                    oper = '+'
                    add_symbols_count += 1
                case 3:
                    oper = '?'
                    add_symbols_count += 1

            part_regex = part_regex[:close_pos] + ')' + oper + part_regex[close_pos:]

            # Обновить индексы в br_pos (при добавлении ')' и операции индексы открывающих
            # скобок справа от них смещаются)
            for i in range(len(br_pos)):
                if br_pos[i] >= close_pos:
                    br_pos[i] += add_symbols_count


        # Удаление *, + или ? с конца, чтоб не было циклов в тупиках
        # И добавление еще одного R или L
        if part_regex[len(part_regex) - 1] in {'*', '+', '?'}:
            part_regex = part_regex[:len(part_regex) - 1]

        L_or_R = random.randint(0, 1)
        match L_or_R:
            case 0:
                part_regex = part_regex[:len(part_regex) - 1] + 'L' + part_regex[-1]
            case 1:
                part_regex = part_regex[:len(part_regex) - 1] + 'R' + part_regex[-1]

        regex_alternate_list.append(part_regex)

    regex = ''
    for reg in regex_alternate_list:
        regex += reg + '|'
    regex = regex[:len(regex) - 1]

    print(regex)

    return regex

# Функция для удаления финальных состояний, которые не являются тупиковыми.
# Если тупиками не считаются вершины, у которых цикл на себе, а дальше переходов нет,
# то надо будет изменить
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

    while True:
        # Генерация регулярки и НКА по ней
        regex = generate_regex()
        init_nfa = init_nfa.from_regex(regex=regex, input_symbols={'L', 'R'})

        # show(init_nfa)

        # Детерминизация
        init_dfa = init_dfa.from_nfa(target_nfa=init_nfa)

        # show(init_dfa)

        # Избавление от нетупиковых финальных состояний, которые могли появиться
        new_final_states = remove_not_dead_end(init_dfa.final_states, init_dfa.transitions)

        if len(new_final_states) != 0:
            break

    # Создание итогового лабиринта
    labyrinth = DFA(
        states=init_dfa.states,
        input_symbols=init_dfa.input_symbols,
        transitions=init_dfa.transitions,
        initial_state=init_dfa.initial_state,
        final_states=new_final_states,
        allow_partial=True
    ).minify()

    print(f"Количество состояний:{len(labyrinth.states)}")

    return labyrinth
