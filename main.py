from src.bigram_matrix import build_bigram_matrix
from src.cfg import CFG
from src.parser.parse_file import parse_grammar


def main():
    with open("rules.txt", "r") as f:
        file_content = f.read()

    rules, terms, nterms = parse_grammar(file_content)
    if rules is None:
        print("Ошибка в переданном файле")
        return

    print("Терминалы в исходной:", terms)
    print("Нетерминалы в исходной:", nterms)

    cfg = CFG(rules, nterms[0], terms, nterms)
    print("Исходная грамматика:")
    cfg.display()

    cfg.convert_to_cnf()
    print("\nГрамматика в ХНФ:")
    cfg.display()

    print("Терминалы:", cfg.terms)
    print("Нетерминалы:", cfg.nterms)


    bigram_matrix, start_terminals, end_terminals = build_bigram_matrix(rules, cfg.terms, cfg.nterms, cfg.start_symbol)

    print("Матрица биграмм:")
    for bigram in bigram_matrix:
        print(bigram)

    print("\nСтартовые терминалы (First(S)):")
    print(start_terminals)

    print("\nФинальные терминалы (Last(S)):")
    print(end_terminals)


if __name__ == "__main__":
    main()
