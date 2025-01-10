from graphviz import Digraph

from src.validator.regex_validator import validate_regex
from src.validator.syntax_validator import validate_syntax
from src.visualise.visualizer import visualize_tree


def main():
    grammar = "(a|\\1)"
    is_valid, msg = validate_syntax(grammar)
    if not is_valid:
        print(is_valid, msg)
        return

    is_valid, tree = validate_regex(grammar)
    print(is_valid)

    graph = Digraph(format="png")
    visualize_tree(tree, graph)
    graph.render("tree_view", view=True)


if __name__ == "__main__":
    main()
