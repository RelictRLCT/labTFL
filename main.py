from src.cfg.bigram_matrix import build_bigram_matrix
from src.cfg.cfg import CFG
from src.generator.checker import cyk
from src.generator.word_generator import generate_word
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

    words_from_lang = set()
    words_not_from_lang = set()
    while (len(words_from_lang) < settings["count_from_lang"]
           or len(words_not_from_lang) < settings["count_not_from_lang"]):
        word = generate_word(bigram_matrix, cfg.terms, start_terminals, end_terminals, settings)
        from_lang = cyk(word, cfg.rules, cfg.start_symbol)
        if from_lang:
            words_from_lang.add(word)
        else:
            words_not_from_lang.add(word)

    print(words_from_lang, '\n', words_not_from_lang)


if __name__ == "__main__":
    main()
