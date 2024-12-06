from src.cfg.bigram_matrix import build_bigram_matrix
from src.cfg.cfg import CFG
from src.generator.generate_tests import generate_tests, print_tests
from src.parser.parse_rules_file import parse_grammar
from src.parser.parse_settings_file import parse_settings
from src.show.show import show_bigram_matrix


def main():
    settings = parse_settings("settings_of_generation.txt")

    with open("rules.txt", "r") as f:
        file_content = f.read()

    rules, terms, nterms = parse_grammar(file_content)
    if rules is None:
        print("Ошибка в переданном файле грамматик")
        return

    cfg = CFG(rules, nterms[0], terms, nterms)
    print("Исходная грамматика:")
    cfg.display()

    cfg.convert_to_cnf()
    print("\nГрамматика в ХНФ:")
    cfg.display()

    bigram_matrix, start_terminals, end_terminals = build_bigram_matrix(rules, cfg.terms, cfg.nterms, cfg.start_symbol)

    show_bigram_matrix(bigram_matrix, start_terminals, end_terminals)
    words_from_lang, words_not_from_lang = generate_tests(cfg, bigram_matrix, settings, start_terminals, end_terminals)
    print_tests(words_from_lang, words_not_from_lang)
    print("\nСлова из языка:", words_from_lang)
    print("Слова не из языка", words_not_from_lang)


if __name__ == "__main__":
    main()
