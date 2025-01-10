from graphviz import Digraph

from src.cfg.cfg_from_tree import cfg_from_tree
from src.validator.regex_validator import validate_regex
from src.validator.syntax_validator import validate_syntax
from src.visualise.visualizer import visualize_tree


def main():
    grammar = "(a|(bb))(a|(?3))"
    is_valid, msg = validate_syntax(grammar)
    if not is_valid:
        print(is_valid, msg)
        return

    is_valid, tree = validate_regex(grammar)
    print(is_valid)

    graph = Digraph(format="png")
    visualize_tree(tree, graph)
    graph.render("tree_view", view=False)

    if is_valid:
        start_sym, gram = cfg_from_tree(tree)

        productions = gram['S']
        prod_strings = [' '.join(prod) if prod else 'ε' for prod in productions]
        print(f"S -> {' | '.join(prod_strings)}")
        for nt in gram:
            if nt != 'S':
                productions = gram[nt]
                prod_strings = [' '.join(prod) if prod else 'ε' for prod in productions]
                print(f"{nt} -> {' | '.join(prod_strings)}")


if __name__ == "__main__":
    main()
