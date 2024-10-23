from automata.fa.dfa import DFA


def make_dfa_from_table(main_prefixes, extended_prefixes, suffixes, table) -> DFA:

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
        final_states=final_states
    )

    return dfa
