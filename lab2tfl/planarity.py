import networkx as nx
from automata.fa.dfa import DFA
from networkx.drawing.nx_pydot import to_pydot

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
        print("Лабиринт планарен")
        return True, None
    else:
        print("Лабиринт не планарен")
        return False, G


def make_planar(dfa: DFA) -> DFA:
    G = nx.DiGraph()

    # Добавляем вершины
    G.add_nodes_from(sorted(dfa.states))

    # Собираем переходы из финальных состояний в ловушку
    final_to_trap_edges = set()
    trap_state = None
    for state in dfa.states:
        transitions = dfa.transitions.get(state, {})
        for symbol in dfa.input_symbols:
            next_state = transitions.get(symbol)
            if next_state is not None:
                G.add_edge(state, next_state, symbol=symbol)
                # Проверяем, является ли это переходом из финального состояния в ловушку
                if state in dfa.final_states and next_state not in dfa.states:
                    final_to_trap_edges.add((state, next_state, symbol))
                    trap_state = next_state  # Сохраняем имя ловушки

    print("Выполняется планаризация")

    # Преобразуем в неориентированный граф и сохраняем атрибуты ребер
    UG = G.to_undirected()
    for u, v, data in G.edges(data=True):
        UG.edges[u, v]['symbol'] = data['symbol']

    # Получаем минимальное остовное дерево с сохранением атрибутов
    T = nx.minimum_spanning_tree(UG, weight=None)

    # Добавляем обратно ребра, сохраняя планарность и атрибуты
    edges_to_consider = list(set(UG.edges()) - set(T.edges()))
    edges_to_consider.sort()

    for edge in edges_to_consider:
        u, v = edge
        data = UG.edges[u, v]
        # Проверяем, является ли ребро переходом из финального состояния в ловушку
        if (u, v, data['symbol']) in final_to_trap_edges:
            # Обязательно добавляем это ребро
            T.add_edge(u, v, **data)
        else:
            # Добавляем ребро и проверяем планарность
            T.add_edge(u, v, **data)
            if not nx.check_planarity(T)[0]:
                T.remove_edge(u, v)
                # Заменяем на петлю в исходной вершине с тем же символом
                T.add_edge(u, u, symbol=data['symbol'])

    # Дополнение переходами из финальных состояний в ловушку
    for u, v, symbol in final_to_trap_edges:
        if not T.has_edge(u, v):
            T.add_edge(u, v, symbol=symbol)

    # Инициализируем new_transitions для всех состояний
    new_transitions = {state: {} for state in sorted(dfa.states)}

    # Добавляем ловушку в список состояний и переходов, если она существует
    if trap_state:
        new_transitions[trap_state] = {}
        all_states = sorted(list(dfa.states) + [trap_state])
    else:
        all_states = sorted(dfa.states)

    # Проход по всем состояниям и символам входного алфавита
    for state in all_states:
        for symbol in sorted(dfa.input_symbols):
            if state in dfa.transitions and symbol in dfa.transitions[state]:
                next_state = dfa.transitions[state][symbol]
                # Проверка, есть ли соответствующее ребро в модифицированном графе
                if T.has_edge(state, next_state) or (state == next_state and T.has_edge(state, state)):
                    new_transitions.setdefault(state, {})[symbol] = next_state
                else:
                    # Ребро удалено, заменяем на цикл
                    new_transitions.setdefault(state, {})[symbol] = state
            else:
                # Добавление петли для отсутствующих переходов
                new_transitions.setdefault(state, {})[symbol] = state

    # Проверка, что переходы из финальных состояний в ловушку сохранены
    for state in dfa.final_states:
        for symbol in sorted(dfa.input_symbols):
            next_state = dfa.transitions.get(state, {}).get(symbol)
            if next_state == trap_state:
                new_transitions[state][symbol] = trap_state

    new_dfa = DFA(
        states=set(new_transitions.keys()),
        input_symbols=dfa.input_symbols,
        transitions=new_transitions,
        initial_state=dfa.initial_state,
        final_states=dfa.final_states,
        allow_partial=False
    )

    return new_dfa

