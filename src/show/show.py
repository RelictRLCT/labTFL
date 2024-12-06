def show_bigram_matrix(bigram_matrix, start_terminals, end_terminals):
    print("\nМатрица биграмм:")
    for bigram in bigram_matrix:
        print(bigram)

    print("\nСтартовые терминалы (First(S)):")
    print(start_terminals)

    print("\nФинальные терминалы (Last(S)):")
    print(end_terminals)
