from collections import defaultdict
from typing import Dict, List

from src.models.tree import Node, SymbolsNode, ConcatNode, AltNode, IterationNode, GroupNode, BackrefNode, GroupLinkNode


def cfg_from_tree(root: Node):
    node_to_nterm: Dict[Node, str] = {}

    # отдельный словарь для групп (group_id -> нетерминал)
    # для ссылок Backref и GroupLink
    group_id_to_nterm: Dict[int, str] = {}

    grammar: Dict[str, List[List[str]]] = defaultdict(list)

    nterm_counter = [1]

    def new_nterm(prefix="X") -> str:
        name = f"{prefix}{nterm_counter[0]}"
        nterm_counter[0] += 1
        return name

    def get_or_make_nterm_for_node(node: Node) -> str:
        """
        Поиск или создание нетерминала для узла
        """
        if node in node_to_nterm:
            return node_to_nterm[node]

        this_nterm = new_nterm()
        node_to_nterm[node] = this_nterm

        # добавление продукций для узла
        build_productions_for_node(node, this_nterm)
        return this_nterm

    def build_productions_for_node(node: Node, nterm: str):
        """
        Построение продукций
        """
        if isinstance(node, SymbolsNode):
            # последовательность символов
            text = node.text
            if text == "":
                grammar[nterm].append([])  # пустая строка
            else:
                # разбиение text на отдельные символы
                rhs = list(text)
                grammar[nterm].append(rhs)

        elif isinstance(node, ConcatNode):
            # конкатенация детей
            children_nterms = []
            for c in node.children:
                c_nt = get_or_make_nterm_for_node(c)
                children_nterms.append(c_nt)
            grammar[nterm].append(children_nterms)

        elif isinstance(node, AltNode):
            # X1 | X2 | ...
            for br in node.branches:
                br_nt = get_or_make_nterm_for_node(br)
                grammar[nterm].append([br_nt])

        elif isinstance(node, IterationNode):
            # *: nterm -> ε | child_nterm nterm
            child_nt = get_or_make_nterm_for_node(node.child)
            grammar[nterm].append([])
            grammar[nterm].append([child_nt, nterm])

        elif isinstance(node, GroupNode):
            # Если группа захватывающая, создание нетерминала Gid
            if node.group_id is not None:
                g_id = node.group_id
                # если ещё не заведён нетерминал для этой группы
                if g_id not in group_id_to_nterm:
                    group_nterm = f"G{g_id}"
                    group_id_to_nterm[g_id] = group_nterm
                    child_nt = get_or_make_nterm_for_node(node.child)
                    grammar[group_nterm].append([child_nt])

                grammar[nterm].append([group_id_to_nterm[g_id]])
            else:
                # (?:...)
                child_nt = get_or_make_nterm_for_node(node.child)
                grammar[nterm].append([child_nt])

        elif isinstance(node, BackrefNode):
            # \num => ссылается на Gnum
            num = node.group_id
            if num not in group_id_to_nterm:
                group_id_to_nterm[num] = f"G{num}"

            grammar[nterm].append([group_id_to_nterm[num]])

        elif isinstance(node, GroupLinkNode):
            # (?num) => аналогично ссылается на Gnum
            num = node.group_id
            if num not in group_id_to_nterm:
                group_id_to_nterm[num] = f"G{num}"
            grammar[nterm].append([group_id_to_nterm[num]])

        else:
            grammar[nterm].append(["ЧЕ ЗА ДИЧЬ"])

    start_symbol = "S"
    node_to_nterm[root] = start_symbol

    build_productions_for_node(root, start_symbol)

    return start_symbol, dict(grammar)