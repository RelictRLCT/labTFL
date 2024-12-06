def get_first_sets(rules: dict, terms: list[str], nterms: list[str]):
    first = {nt: set() for nt in nterms}
    changed = True
    while changed:
        changed = False
        for nt in nterms:
            for production in rules.get(nt, []):
                symbol = production[0]
                # Если первый символ - терминал
                if symbol in terms:
                    if symbol not in first[nt]:
                        first[nt].add(symbol)
                        changed = True
                else:
                    # Если первый символ - нетерминал
                    before = len(first[nt])
                    first[nt].update(first[symbol])
                    if len(first[nt]) > before:
                        changed = True
    return first


def get_follow_sets(rules: dict, terms: list[str], nterms: list[str], first):
    follow = {nt: set() for nt in nterms}
    changed = True
    while changed:
        changed = False
        for nt in nterms:
            for production in rules.get(nt, []):
                for i, symbol in enumerate(production):
                    if symbol in nterms:
                        if i + 1 < len(production):
                            next_symbol = production[i + 1]
                            if next_symbol in terms:
                                # Следующий символ - терминал
                                if next_symbol not in follow[symbol]:
                                    follow[symbol].add(next_symbol)
                                    changed = True
                            else:
                                # Следующий символ - нетерминал
                                before = len(follow[symbol])
                                follow[symbol].update(first[next_symbol])
                                if len(follow[symbol]) > before:
                                    changed = True
                        else:
                            # Символ в конце продукции
                            before = len(follow[symbol])
                            follow[symbol].update(follow[nt])
                            if len(follow[symbol]) > before:
                                changed = True
    return follow


def get_last_sets(rules: dict, terms: list[str], nterms: list[str]):
    last = {nt: set() for nt in nterms}
    changed = True
    while changed:
        changed = False
        for nt in nterms:
            for production in rules.get(nt, []):
                symbol = production[-1]
                # Если последний символ - терминал
                if symbol in terms:
                    if symbol not in last[nt]:
                        last[nt].add(symbol)
                        changed = True
                else:
                    # Если последний символ - нетерминал
                    before = len(last[nt])
                    last[nt].update(last[symbol])
                    if len(last[nt]) > before:
                        changed = True
    return last


def get_precede_sets(rules: dict, terms: list[str], nterms: list[str], last):
    precede = {nt: set() for nt in nterms}
    changed = True
    while changed:
        changed = False
        for nt in nterms:
            for production in rules.get(nt, []):
                for i in range(1, len(production)):
                    symbol = production[i]
                    prev_symbol = production[i - 1]
                    if symbol in nterms:
                        if prev_symbol in terms:
                            # Предыдущий символ - терминал
                            if prev_symbol not in precede[symbol]:
                                precede[symbol].add(prev_symbol)
                                changed = True
                        elif prev_symbol in nterms:
                            # Предыдущий символ - нетерминал
                            before = len(precede[symbol])
                            precede[symbol].update(last[prev_symbol])
                            if len(precede[symbol]) > before:
                                changed = True
    return precede


def build_bigram_matrix(rules: dict, terms: list[str], nterms: list[str], start_symbol):
    first = get_first_sets(rules, terms, nterms)
    follow = get_follow_sets(rules, terms, nterms, first)
    last = get_last_sets(rules, terms, nterms)
    precede = get_precede_sets(rules, terms, nterms, last)

    bigram_matrix = set()

    # Условие 1: гамма1 и гамма2 рядом в правиле
    for productions in rules.values():
        for prod in productions:
            for i in range(len(prod) - 1):
                sym1 = prod[i]
                sym2 = prod[i + 1]
                if sym1 in terms and sym2 in terms:
                    bigram_matrix.add((sym1, sym2))

    # Условие 2: гамма1 в Last(A1) и гамма2 в Follow(A1)
    for A1 in nterms:
        for gamma1 in last[A1]:
            if gamma1 in terms:
                for gamma2 in follow[A1]:
                    if gamma2 in terms:
                        bigram_matrix.add((gamma1, gamma2))

    # Условие 3: гамма1 в Precede(A2) и гамма2 в First(A2) (судя по всему, ошибка в презе)
    for A2 in nterms:
        for gamma1 in precede[A2]:
            if gamma1 in terms:
                for gamma2 in first[A2]:
                    if gamma2 in terms:
                        bigram_matrix.add((gamma1, gamma2))

    # Условие 4: гамма1 в Last(A1), гамма2 в First(A2), и A2 в Follow(A1) (похоже, тоже ошибка в презе)
    for A1 in nterms:
        for gamma1 in last[A1]:
            if gamma1 in terms:
                for A2 in follow[A1]:
                    if A2 in nterms:
                        for gamma2 in first[A2]:
                            if gamma2 in terms:
                                bigram_matrix.add((gamma1, gamma2))

    start_terminals = first[start_symbol]
    end_terminals = last[start_symbol]

    return bigram_matrix, start_terminals, end_terminals
