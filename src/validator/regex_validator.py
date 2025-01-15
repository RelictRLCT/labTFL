from src.models.tree import Node, GroupLinkNode, BackrefNode, GroupNode, ConcatNode, AltNode, IterationNode
from src.validator.parser import RegexToTree, analyze_expr


def validate_regex(s: str) -> (bool, Node):
    parser = RegexToTree(s)
    try:
        tree_root = parser.parse()
    except ValueError as e:
        print(f"ОШИБКА!!!!!!!!!!!!!!!! {e}")
        return False, None

    if parser.group_count > 9:
        return False, None

    # Все \num и (?num) должны быть <= parser.group_count
    def check_group_exists(node: Node) -> bool:
        if isinstance(node, BackrefNode):
            # \num
            return 1 <= node.group_id <= parser.group_count
        if isinstance(node, GroupLinkNode):
            # (?num)
            return 1 <= node.group_id <= parser.group_count
        if isinstance(node, GroupNode):
            return check_group_exists(node.child)
        if isinstance(node, ConcatNode):
            return all(check_group_exists(ch) for ch in node.children)
        if isinstance(node, AltNode):
            return all(check_group_exists(br) for br in node.branches)
        if isinstance(node, IterationNode):
            return check_group_exists(node.child)
        return True

    if not check_group_exists(tree_root):
        return False, None

    # Проверка инициализации на момент обращения
    memo = {}
    memo_status = {}
    valid, final_set = analyze_expr(tree_root, set(), parser.group_definitions, memo, memo_status)

    return valid, tree_root