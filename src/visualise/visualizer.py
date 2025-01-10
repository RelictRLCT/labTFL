from src.models.tree import Node, ConcatNode, AltNode, GroupNode, SymbolsNode, BackrefNode, GroupLinkNode, \
    IterationNode

from graphviz import Digraph


def visualize_tree(node: Node, graph: Digraph = None, parent_id: str = None, node_id: int = 0) -> int:
    if graph is None:
        graph = Digraph(format='png')
        graph.attr(rankdir='TB')

    current_id = f"node{node_id}"
    node_id += 1

    if isinstance(node, ConcatNode):
        label = "Concat"
    elif isinstance(node, AltNode):
        label = "Alt"
    elif isinstance(node, GroupNode):
        label = f"Group (id={node.group_id})" if node.group_id is not None else "(?:)"
    elif isinstance(node, SymbolsNode):
        label = f"Symbols: {node.text}"
    elif isinstance(node, BackrefNode):
        label = f"Backref: \\{node.group_id}"
    elif isinstance(node, GroupLinkNode):
        label = f"Subroutine: (?{node.group_id})"
    elif isinstance(node, IterationNode):
        label = f"Iteration (*)"
    else:
        label = "Unknown"

    graph.node(current_id, label)

    if parent_id:
        graph.edge(parent_id, current_id)

    if isinstance(node, ConcatNode):
        for child in node.children:
            node_id = visualize_tree(child, graph, current_id, node_id)

    elif isinstance(node, AltNode):
        for branch in node.branches:
            node_id = visualize_tree(branch, graph, current_id, node_id)

    elif isinstance(node, GroupNode):
        node_id = visualize_tree(node.child, graph, current_id, node_id)

    elif isinstance(node, IterationNode):
        node_id = visualize_tree(node.child, graph, current_id, node_id)

    return node_id
