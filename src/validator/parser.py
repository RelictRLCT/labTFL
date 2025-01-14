import re
from collections.abc import Set
from enum import Enum
from typing import Dict, Tuple

from src.models.tree import Node, AltNode, SymbolsNode, ConcatNode, IterationNode, GroupNode, GroupLinkNode, \
    BackrefNode


class VisitStatus(Enum):
    IN_PROGRESS = 1
    DONE = 2


class RegexToTree:
    def __init__(self, s: str):
        self.regex = s
        self.i = 0
        self.length = len(s)
        self.group_count = 0
        self.group_definitions = {}

    def parse(self) -> Node:
        return self.parse_alternative()

    def parse_alternative(self) -> Node:
        branches = [self.parse_concatenation()]
        while self.i < self.length and self.regex[self.i] == '|':
            self.i += 1
            branches.append(self.parse_concatenation())
        if len(branches) == 1:
            return branches[0]
        else:
            return AltNode(branches)

    def parse_concatenation(self) -> Node:
        nodes = []
        while (self.i < self.length) and (self.regex[self.i] not in (')', '|', '*')):
            node = self.parse_repetition()
            nodes.append(node)
        if not nodes:
            return SymbolsNode("")
        if len(nodes) == 1:
            return nodes[0]
        return ConcatNode(nodes)

    def parse_repetition(self) -> Node:
        operation_node = self.parse_operation()

        # Если есть * после операции
        while self.i < self.length and self.regex[self.i] == '*':
            c = self.regex[self.i]
            if c == '*':
                operation_node = IterationNode(operation_node)
            self.i += 1
        return operation_node

    def parse_operation(self) -> Node:
        """
          (...) - захватывающая группа
          (?:...) - незахватывающая группа
          (?num) - ссылка на группу
          \num - захваченная строка
        """
        if self.i >= self.length:
            return SymbolsNode("")

        c = self.regex[self.i]

        # '('
        if c == '(':
            # проверка на (?:
            if self.i + 3 <= self.length and self.regex[self.i:self.i + 3] == '(?:':
                # незахватывающая
                self.i += 3
                sub = self.parse_alternative()
                self.i += 1
                return GroupNode(None, sub)

            # проверка на (?num)
            if self.i+2 < self.length and self.regex[self.i:self.i + 2] == '(?':
                match = re.match(r'\(\?(\d+)\)', self.regex[self.i:])
                if match:
                    k = int(match.group(1))
                    self.i += len(match.group(0))
                    return GroupLinkNode(k)

            # иначе - обычная захватывающая группа
            self.i += 1
            self.group_count += 1
            gr_id = self.group_count
            sub = self.parse_alternative()
            self.i += 1
            # Запись подвыражения в group_definitions
            self.group_definitions[gr_id] = sub
            return GroupNode(gr_id, sub)

        # '\'
        if c == '\\':
            k = int(self.regex[self.i + 1])
            self.i += 2
            return BackrefNode(k)

        # Иначе символы
        txt = self.regex[self.i]
        self.i += 1
        return SymbolsNode(txt)


def analyze_expr(
    node,
    init_set: Set[int],
    group_defs: Dict[int, 'Node'],
    res: Dict[Tuple['Node', frozenset], Tuple[bool, Set[int]]],
    status: Dict[Tuple['Node', frozenset], VisitStatus]
) -> Tuple[bool, Set[int]]:

    key = (node, frozenset(init_set))

    # Если уже что-то знаем о статусе узла
    if key in status:
        if status[key] == VisitStatus.DONE:
            # Уже полностью обработано
            return res[key]
        elif status[key] == VisitStatus.IN_PROGRESS:
            # Рекурсия на самом себе
            return True, init_set

    status[key] = VisitStatus.IN_PROGRESS

    if isinstance(node, SymbolsNode):
        # Просто символы
        result = (True, init_set)

    elif isinstance(node, BackrefNode):
        # Надо, чтобы num был в init_set
        if node.group_id in init_set:
            result = (True, init_set)
        else:
            # num не инициализирован
            result = (False, init_set)

    elif isinstance(node, GroupLinkNode):
        # (?num)
        body = group_defs.get(node.group_id)
        if body is None:
            # Нет такой группы
            result = (False, init_set)
        else:
            valid_sub, final_sub = analyze_expr(body, init_set, group_defs, res, status)
            result = (valid_sub, init_set)

    elif isinstance(node, GroupNode):
        if node.group_id is None:
            # (?:...)
            valid_sub, final_sub = analyze_expr(node.child, init_set, group_defs, res, status)
            result = (valid_sub, final_sub)
        else:
            # (...)
            valid_sub, final_sub = analyze_expr(node.child, init_set, group_defs, res, status)
            if not valid_sub:
                result = (False, init_set)
            else:
                # При выходе из группы num добавляем её в final_set
                new_set = set(final_sub)
                new_set.add(node.group_id)
                result = (True, new_set)

    elif isinstance(node, ConcatNode):
        # Конкатенация
        current_set = init_set
        valid = True
        for child in node.children:
            valid_child, set_child = analyze_expr(child, current_set, group_defs, res, status)
            if not valid_child:
                valid = False
                break
            current_set = set_child
        result = (valid, current_set)

    elif isinstance(node, AltNode):
        # Альтернатива, все ветви должны быть корректны
        # final_set - пересечение множеств из каждой ветви
        final_sets = []
        valid_all = True
        for branch in node.branches:
            vb, fb = analyze_expr(branch, init_set, group_defs, res, status)
            if not vb:
                valid_all = False
                break
            final_sets.append(fb)
        if not valid_all or not final_sets:
            result = (False, init_set)
        else:
            common = set(final_sets[0])
            for fs in final_sets[1:]:
                common.intersection_update(fs)
            result = (True, common)

    elif isinstance(node, IterationNode):
        valid_child, set_child = analyze_expr(node.child, init_set, group_defs, res, status)
        if not valid_child:
            result = (False, init_set)
        else:
            combined = set(init_set).intersection(set_child)
            result = (True, combined)

    else:
        result = (False, init_set)

    res[key] = result
    status[key] = VisitStatus.DONE
    return result