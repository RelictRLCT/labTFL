from automata.fa.dfa import DFA
from show import show

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
    #     ('ε', 'ε'): '-',
    #     ('ε', 'L'): '-',
    #     ('ε', 'RL'): '-',
    #     ('ε', 'LRL'): '+',
    #
    #     ('R', 'ε'): '+',
    #     ('R', 'L'): '-',
    #     ('R', 'RL'): '-',
    #     ('R', 'LRL'): '-',
    #
    #     ('L', 'ε'): '-',
    #     ('L', 'L'): '-',
    #     ('L', 'RL'): '+',
    #     ('L', 'LRL'): '-',
    #
    #     ('RL', 'ε'): '-',
    #     ('RL', 'L'): '+',
    #     ('RL', 'RL'): '-',
    #     ('RL', 'LRL'): '-',
    #
    #     ('RR', 'ε'): '-',
    #     ('RR', 'L'): '-',
    #     ('RR', 'RL'): '-',
    #     ('RR', 'LRL'): '-',
    #
    #     ('LL', 'ε'): '-',
    #     ('LL', 'L'): '-',
    #     ('LL', 'RL'): '-',
    #     ('LL', 'LRL'): '+',
    #
    #     ('LR', 'ε'): '-',
    #     ('LR', 'L'): '+',
    #     ('LR', 'RL'): '-',
    #     ('LR', 'LRL'): '-',
    #
    #     ('RLL', 'ε'): '+',
    #     ('RLL', 'L'): '-',
    #     ('RLL', 'RL'): '-',
    #     ('RLL', 'LRL'): '-',
    #
    #     ('RLR', 'ε'): '-',
    #     ('RLR', 'L'): '-',
    #     ('RLR', 'RL'): '-',
    #     ('RLR', 'LRL'): '-',
    #
    #     ('RRL', 'ε'): '-',
    #     ('RRL', 'L'): '-',
    #     ('RRL', 'RL'): '-',
    #     ('RRL', 'LRL'): '-',
    #
    #     ('RRR', 'ε'): '-',
    #     ('RRR', 'L'): '-',
    #     ('RRR', 'RL'): '-',
    #     ('RRR', 'LRL'): '-',
    # }

    # Все префиксы
    prefixes = main_prefixes + extended_prefixes

    # Функция для получения строки таблицы для префикса
    def get_table_string(prefix):
        return ''.join([table.get((prefix, suffix), '-') for suffix in suffixes])

    # Определение эквивалентных классов по основной части таблицы
    main_strings = {}
    for prefix in main_prefixes:
        table_string = get_table_string(prefix)
        main_strings[prefix] = table_string

    # Соответствие строк и состояний
    table_string_to_state = {}
    for idx, (prefix, table_string) in enumerate(main_strings.items()):
        state_name = f'q{idx}'
        table_string_to_state[table_string] = state_name

    # Соответствие префиксов и состояний
    prefix_to_state = {}
    for prefix in prefixes:
        table_string = get_table_string(prefix)
        # Ищем эквивалентный класс в основной части
        if table_string in table_string_to_state:
            state = table_string_to_state[table_string]
        else:
            # Если не найдено, создается ошибочное состояние (не должно происходить)
            state = 'ERROR'
        prefix_to_state[prefix] = state

    # Построение переходов
    transitions = {}
    # Обработка состояний, соответствующих префиксам из основной части
    for prefix in main_prefixes:
        current_state = prefix_to_state[prefix]
        transitions.setdefault(current_state, {})
        for symbol in ['L', 'R']:
            new_prefix = ('' if prefix == 'ε' else prefix) + symbol
            # Проверка, присутствует ли новый префикс в списке префиксов
            if new_prefix in prefixes:
                # Получение строки таблицы нового префикса
                new_features = get_table_string(new_prefix)
                # Поиск соответствующего состояния по строке
                if new_features in table_string_to_state:
                    next_state = table_string_to_state[new_features]
                else:
                    next_state = 'ERROR'
            else:
                next_state = 'ERROR'
            transitions[current_state][symbol] = next_state

    if 'ERROR' in prefix_to_state.values():
        transitions['ERROR'] = {'L': 'ERROR', 'R': 'ERROR'}

    # Определение начального и конечных состояний
    initial_state = prefix_to_state['ε']
    final_states = set()
    for prefix in main_prefixes:
        if table.get((prefix, 'ε'), '-') == '+':
            final_states.add(prefix_to_state[prefix])

    dfa = DFA(
        states=set(transitions.keys()),
        input_symbols={'L', 'R'},
        transitions=transitions,
        initial_state=initial_state,
        final_states=final_states,
        allow_partial=False
    )

    return dfa


if __name__ == "__main__":
    dfa123 = make_dfa_from_table('sdf')
    show(dfa123)
