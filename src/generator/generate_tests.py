import time
from src.cfg.cfg import CFG
from src.generator.checker import cyk
from src.generator.word_generator import generate_word


def generate_tests(
        cfg: CFG,
        bigram_matrix: set,
        settings: dict,
        start_terminals: list[str],
        end_terminals: list[str]
) -> (set[str], set[str]):
    words_from_lang = set()
    words_not_from_lang = set()
    start_time = time.time()
    while (
            len(words_from_lang) < settings["count_from_lang"]
            or
            len(words_not_from_lang) < settings["count_not_from_lang"]
    ):
        elapsed_time = time.time() - start_time
        if elapsed_time > settings["max_time"]:
            print("Максимальное время генерации вышло. "
                  "\nПроверьте грамматику или измените настройки случайного выбора терминалов. "
                  "\nСгенерированные слова все равно будут выведены в файл")
            break
        word = generate_word(bigram_matrix, cfg.terms, start_terminals, end_terminals, settings)
        from_lang = cyk(word, cfg.rules, cfg.start_symbol)
        if from_lang:
            if len(words_from_lang) < settings["count_from_lang"]:
                words_from_lang.add(word)
        else:
            if len(words_not_from_lang) < settings["count_not_from_lang"]:
                words_not_from_lang.add(word)
    return words_from_lang, words_not_from_lang
