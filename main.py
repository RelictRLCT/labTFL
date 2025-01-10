from graphviz import Digraph

from src.cfg.cfg_from_tree import cfg_from_tree
from src.validator.regex_validator import validate_regex
from src.validator.syntax_validator import validate_syntax
from src.visualise.visualizer import visualize_tree


def check_grammar(grammar: str, show: bool = True):
    is_valid, msg = validate_syntax(grammar)
    if not is_valid:
        print("Синтаксис регекса некорректен.", msg)
        return

    is_valid, tree = validate_regex(grammar)

    if show:
        graph = Digraph(format="png")
        visualize_tree(tree, graph)
        graph.render("tree_view", view=False)

    if is_valid:
        print("Регекс корректен")
        start_sym, gram = cfg_from_tree(tree)

        productions = gram['S']
        prod_strings = [' '.join(prod) if prod else 'ε' for prod in productions]
        print(f"S -> {' | '.join(prod_strings)}")
        for nt in gram:
            if nt != 'S':
                productions = gram[nt]
                prod_strings = [' '.join(prod) if prod else 'ε' for prod in productions]
                print(f"{nt} -> {' | '.join(prod_strings)}")
    else:
        print("Регекс некорректен")


def main():
    tests = int(
                input(
                    "Выберите режим: \n1 - проверка регекса из файла regex.txt\n"
                    "2 - автоматический прогон тестов из файлов tests_correct.txt "
                    "и tests_incorrect.txt\n"
                )
            )
    match tests:
        case 1:
            with open('regex.txt', 'r') as f:
                grammar = f.readline().strip()
                print(f"Переданный регекс: {grammar}")
            check_grammar(grammar)
        case 2:
            print("\nКорректные тесты:\n")
            with open('tests_correct.txt', 'r') as f:
                for grammar in f:
                    grammar = grammar.strip()
                    if grammar:
                        print(f"Переданный регекс: {grammar}")
                        check_grammar(grammar, show=False)
                        print()

            print("\nНекорректные тесты:\n")
            with open('tests_incorrect.txt', 'r') as f:
                for grammar in f:
                    grammar = grammar.strip()
                    if grammar:
                        print(f"Переданный регекс: {grammar}")
                        check_grammar(grammar, show=False)
                        print()
        case _:
            print("Неверный режим")


if __name__ == "__main__":
    main()
