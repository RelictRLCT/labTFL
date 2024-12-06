def cyk(word, rules, start_symbol):
    n = len(word)
    P = [[set() for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for A, productions in rules.items():
            for prod in productions:
                if len(prod) == 1 and prod[0] == word[i]:
                    P[i][i].add(A)

    for l in range(2, n + 1):
        for i in range(n - l + 1):
            j = i + l - 1
            for k in range(i, j):
                for A, productions in rules.items():
                    for prod in productions:
                        if len(prod) == 2:
                            B, C = prod
                            if B in P[i][k] and C in P[k + 1][j]:
                                P[i][j].add(A)

    return start_symbol in P[0][n-1]
