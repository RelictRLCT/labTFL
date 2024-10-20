from automata.fa.dfa import DFA
from automata.fa.nfa import NFA
from matplotlib import pyplot as plt
from typing import Union
from pathlib import Path

def show(automata: Union[DFA, NFA], name_of_file='labyrinth.png'):
    Path("../images").mkdir(parents=True, exist_ok=True)
    automata.show_diagram().draw('../images/' + name_of_file, prog='dot')
    #img = plt.imread('../images/' + name_of_file)
    #plt.imshow(img)
    #plt.show()
