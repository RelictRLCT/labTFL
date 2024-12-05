from src.cfg import CFG


def main():
    # rules = {
    #     "S": [["A", "B", "C"], ["B", "C"]],
    #     "A": [["a", "B", "a"]],
    #     "B": [["b"]],
    #     "C": [["c"]],
    #     "D": [["A", "D"]],  # Бесполезное
    #     "E": [["A"]],       # Цепное
    # }

    rules = {
        "S": [["A", "B", "C", "D", "a"], ["B", "C", "C"], ["D"]],
        "A": [["B"]],
        "B": [["C"]],
        "C": [["c"]],
        "D": [["D"]]
    }

    terms = ["c"]
    nterms = ["S", "A", "B", "C", "D"]

    start_symbol = "S"

    cfg = CFG(rules, start_symbol, terms, nterms)
    print("Исходная грамматика:")
    cfg.display()
    print(cfg.nterms)

    cfg.convert_to_cnf()
    print("\nГрамматика в ХНФ:")
    cfg.display()
    print(cfg.nterms)


if __name__ == "__main__":
    main()
