from typing import List, Optional


class Node:
    """Базовый класс для всех узлов дерева"""
    pass


class ConcatNode(Node):
    """Последовательность нескольких подвыражений"""
    def __init__(self, children: List['Node']):
        self.children = children


class AltNode(Node):
    """Альтернатива"""
    def __init__(self, branches: List['Node']):
        self.branches = branches


class GroupNode(Node):
    """
    Захватывающая группа
    Если group_id=None, то это незахватывающая группа (?:...)
    """
    def __init__(self, group_id: Optional[int], child: 'Node'):
        self.group_id = group_id
        self.child = child


class SymbolsNode(Node):
    """Простые символы"""
    def __init__(self, text: str):
        self.text = text


class BackrefNode(Node):
    """Ссылка на захваченную строку \num"""
    def __init__(self, group_id: int):
        self.group_id = group_id


class GroupLinkNode(Node):
    """Ссылка на группу (?num)"""
    def __init__(self, group_id: int):
        self.group_id = group_id


class IterationNode(Node):
    """Итерация [reg]*"""
    def __init__(self, child: Node):
        self.child = child
