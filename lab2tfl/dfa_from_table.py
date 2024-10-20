from automata.fa.dfa import DFA


def make_dfa_from_table(main_prefixes, extended_prefixes, suffixes, table) -> DFA:
    # # Основная часть таблицы
    # main_prefixes = ['ε', 'R', 'L', 'RL', 'RR']
    # # Расширенная часть таблицы
    # extended_prefixes = ['LL', 'LR', 'RLL', 'RLR', 'RRL', 'RRR']
    # # Все префиксы
    # prefixes = main_prefixes + extended_prefixes
    # suffixes = ['ε', 'L', 'RL', 'LRL']
    #
    # # Таблица признаков
    # table = {
    #     ('ε', 'ε'): '0',
    #     ('ε', 'L'): '0',
    #     ('ε', 'RL'): '0',
    #     ('ε', 'LRL'): '1',
    #
    #     ('R', 'ε'): '1',
    #     ('R', 'L'): '0',
    #     ('R', 'RL'): '0',
    #     ('R', 'LRL'): '0',
    #
    #     ('L', 'ε'): '0',
    #     ('L', 'L'): '0',
    #     ('L', 'RL'): '1',
    #     ('L', 'LRL'): '0',
    #
    #     ('RL', 'ε'): '0',
    #     ('RL', 'L'): '1',
    #     ('RL', 'RL'): '0',
    #     ('RL', 'LRL'): '0',
    #
    #     ('RR', 'ε'): '0',
    #     ('RR', 'L'): '0',
    #     ('RR', 'RL'): '0',
    #     ('RR', 'LRL'): '0',
    #
    #     ('LL', 'ε'): '0',
    #     ('LL', 'L'): '0',
    #     ('LL', 'RL'): '0',
    #     ('LL', 'LRL'): '1',
    #
    #     ('LR', 'ε'): '0',
    #     ('LR', 'L'): '1',
    #     ('LR', 'RL'): '0',
    #     ('LR', 'LRL'): '0',
    #
    #     ('RLL', 'ε'): '1',
    #     ('RLL', 'L'): '0',
    #     ('RLL', 'RL'): '0',
    #     ('RLL', 'LRL'): '0',
    #
    #     ('RLR', 'ε'): '0',
    #     ('RLR', 'L'): '0',
    #     ('RLR', 'RL'): '0',
    #     ('RLR', 'LRL'): '0',
    #
    #     ('RRL', 'ε'): '0',
    #     ('RRL', 'L'): '0',
    #     ('RRL', 'RL'): '0',
    #     ('RRL', 'LRL'): '0',
    #
    #     ('RRR', 'ε'): '0',
    #     ('RRR', 'L'): '0',
    #     ('RRR', 'RL'): '0',
    #     ('RRR', 'LRL'): '0',
    # }


    prefixes = main_prefixes + extended_prefixes

    def get_table_string(prefix):
        return ''.join([table.get((prefix, suffix), '0') for suffix in suffixes])

    # Определение эквивалентных классов по всем префиксам
    all_strings = {}
    for prefix in prefixes:
        table_string = get_table_string(prefix)
        all_strings[prefix] = table_string

    # Соответствие строк и состояний
    table_string_to_state = {}
    state_counter = 0
    for table_string in set(all_strings.values()):
        state_name = f'q{state_counter}'
        table_string_to_state[table_string] = state_name
        state_counter += 1

    # Соответствие префиксов и состояний
    prefix_to_state = {}
    for prefix in prefixes:
        table_string = all_strings[prefix]
        state = table_string_to_state[table_string]
        prefix_to_state[prefix] = state

    # Построение переходов
    transitions = {}
    for prefix in prefixes:
        current_state = prefix_to_state[prefix]
        transitions.setdefault(current_state, {})
        for symbol in ['L', 'R']:
            new_prefix = ('' if prefix == 'ε' else prefix) + symbol
            if new_prefix in prefixes:
                next_state = prefix_to_state[new_prefix]
                transitions[current_state][symbol] = next_state
            else:
                # Переход остаётся не определённым (partial DFA)
                pass

    # Определение начального и конечных состояний
    initial_state = prefix_to_state['ε']
    final_states = set()
    for prefix in prefixes:
        if table.get((prefix, 'ε'), '0') == '1':
            final_states.add(prefix_to_state[prefix])

    # Создание DFA
    dfa = DFA(
        states=set(transitions.keys()),
        input_symbols={'L', 'R'},
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
        allow_partial=True
    )

    return dfa
