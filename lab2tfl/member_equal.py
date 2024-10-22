from automata.fa.dfa import DFA
from show import show


def equal_labyrinths(labyrinth: DFA, learner_dfa: DFA) -> (str, bool):

    dfa = labyrinth.symmetric_difference(learner_dfa)

    if dfa.isempty():
        # Эквивалентны
        return None, None
    else:
        dfa = labyrinth.difference(learner_dfa)
        if dfa.isempty():
            k = 0
            while True:
                try:
                    return dfa.random_word(k), False
                except ValueError:
                    k += 1

        k = 0
        while True:
            try:
                return dfa.random_word(k), True
            except ValueError:
                k += 1


def membership(labyrinth: DFA, word: str) -> bool:
    if len(word) > 0:
        if word[0] == 'ε':
            word = word[1:]
    return labyrinth.accepts_input(word)
