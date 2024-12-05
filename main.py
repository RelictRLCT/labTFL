from src.cfg import CFG
from src.parser.parse_file import parse_grammar


def main():
    with open("rules.txt", "r") as f:
        file_content = f.read()

    rules, terms, nterms = parse_grammar(file_content)
    if rules is None:
        print("Ошибка в переданном файле")
        return

    print("Терминалы:", terms)
    print("Нетерминалы:", nterms)

    cfg = CFG(rules, nterms[0], terms, nterms)
    print("Исходная грамматика:")
    cfg.display()

    cfg.convert_to_cnf()
    print("\nГрамматика в ХНФ:")
    cfg.display()


if __name__ == "__main__":
    main()
