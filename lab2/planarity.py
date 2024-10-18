import networkx as nx
from automata.fa.dfa import DFA
from show import show
from networkx.drawing.nx_pydot import write_dot, to_pydot

def save_graph_image(G, filename):
    pydot_graph = to_pydot(G)
    pydot_graph.write_png(filename)

def check_planarity(dfa: DFA) -> (bool, DFA):
    G = nx.DiGraph()

    # Добавляем вершины
    G.add_nodes_from(dfa.states)

    # Добавляем ребра с атрибутами
    for state in dfa.states:
        transitions = dfa.transitions.get(state, {})
        for symbol, next_state in transitions.items():
            G.add_edge(state, next_state, symbol=symbol)

    # Проверка планарности
    is_planar, _ = nx.check_planarity(G.to_undirected())
    if is_planar:
        # save_graph_image(G.to_undirected(), '../images/original_graph.png')
        print("Лабиринт планарен")
        return True, None
    else:
        print("Лабиринт не планарен")
        return False, G


def make_planar(dfa: DFA) -> DFA:
    G = nx.DiGraph()

    # Добавляем вершины
    G.add_nodes_from(dfa.states)

    # Добавляем ребра с атрибутами
    for state in dfa.states:
        transitions = dfa.transitions.get(state, {})
        for symbol, next_state in transitions.items():
            G.add_edge(state, next_state, symbol=symbol)

    # save_graph_image(G, 'original_graph.png')

    print("Выполняется планаризация")

    # Преобразуем в неориентированный граф и сохраняем атрибуты ребер
    UG = G.to_undirected()
    for u, v, data in G.edges(data=True):
        UG.edges[u, v]['symbol'] = data['symbol']

    # Получаем минимальное остовное дерево с сохранением атрибутов
    T = nx.minimum_spanning_tree(UG, weight=None)

    # Добавляем обратно ребра, сохраняя планарность и атрибуты
    edges_to_consider = set(UG.edges()) - set(T.edges())
    for edge in edges_to_consider:
        u, v = edge
        data = UG.edges[u, v]
        T.add_edge(u, v, **data)
        if not nx.check_planarity(T)[0]:
            T.remove_edge(u, v)
            # Заменяем на петлю в исходной вершине с тем же символом
            T.add_edge(u, u, symbol=data['symbol'])

    # Инициализируем new_transitions для всех состояний
    new_transitions = {state: {} for state in dfa.states}

    # Проходим по всем состояниям и символам входного алфавита
    for state in dfa.states:
        for symbol in dfa.input_symbols:
            # Получаем целевое состояние в исходном ДКА
            next_state = dfa.transitions.get(state, {}).get(symbol)
            if next_state is not None:
                # Проверяем, есть ли соответствующее ребро в модифицированном графе
                if T.has_edge(state, next_state) or (state == next_state and T.has_edge(state, state)):
                    new_transitions[state][symbol] = next_state
                else:
                    # Ребро удалено, заменяем на петлю
                    new_transitions[state][symbol] = state
            else:
                # Петля
                new_transitions[state][symbol] = state

        # Проверяем, есть ли хотя бы один переход из состояния
        if not new_transitions[state]:
            # Если нет переходов, добавляем петлю на произвольный символ
            symbol = next(iter(dfa.input_symbols))
            new_transitions[state][symbol] = state

    # Создаем новый ДКА с обновленными переходами
    new_dfa = DFA(
        states=dfa.states,
        input_symbols=dfa.input_symbols,
        transitions=new_transitions,
        initial_state=dfa.initial_state,
        final_states=dfa.final_states,
        allow_partial=False
    )

    return new_dfa
