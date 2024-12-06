import random

def generate_word(
        bigram_matrix: set,
        terms: list[str],
        start_terminals: list[str],
        end_terminals: list[str],
        possibility_of_not_con=0.5,
        max_length=20
) -> (str, bool):
    current = random.choice(list(start_terminals))
    word = [current]
    is_from_language = True
    # Если не было случайных переходов или не завершались досрочно,
    # то слово сразу принадлежит языку и можно не проверять в дальнейшем

    while True:
        if current in end_terminals:
            can_continue = False
            for et in end_terminals:
                for pair in bigram_matrix:
                    if pair[0] == et:
                        can_continue = True # Можно продолжить дальше с вероятностью
            if not can_continue:
                break
            if random.random() < 0.5:
                # То есть, даже если мы в финальном терминале, можем с некоторой
                # вероятностью продолжить генерацию, если у этого терминала есть следующий
                # в матрице биграмм
                break

        if len(word) >= max_length:
            is_from_language = False
            break

        # Возможность выбора случайного следующего терминала
        if random.random() < possibility_of_not_con:
            is_from_language = False # уже непонятно, откуда слово
            next_term = random.choice(terms)
        else:
            possible_next = []
            for pair in bigram_matrix:
                if pair[0] == current:
                    possible_next.append(pair[1])

            if not possible_next:
                # Если вдруг нет вариантов
                next_term = random.choice(terms)
                is_from_language = False
            else:
                next_term = random.choice(possible_next)

        word.append(next_term)
        current = next_term

    return word, is_from_language
