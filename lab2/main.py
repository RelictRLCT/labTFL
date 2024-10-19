from automata.fa.dfa import DFA
from generator import generate_labyrinth
from lab2.member_equal import equal_labyrinths
from planarity import make_planar, check_planarity
from show import show
from member_equal import membership

import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Генератор планарного лабиринта')
    parser.add_argument('-m', type=str, default='No', help='Выполнить минимизацию (-m yes)')
    parser.add_argument('-p', type=str, default='No', help='Выполнить планаризацию (-p yes)')
    args = parser.parse_args()
    print(f'Аргументы: {args.m}, {args.p}')


    labyrinth: DFA = generate_labyrinth()

    # labyrinth = labyrinth.minify()
    while not check_planarity(labyrinth)[0]:
        labyrinth = make_planar(labyrinth) # .minify()

    print(f"Итоговое количество состояний: {len(labyrinth.states)}")
    show(labyrinth)

    while True:
        prompt = input().split()
        if len(prompt) < 2:
            print('Неверный ввод')
            continue
        instruction, arg = prompt[0], prompt[1]
        match instruction:
            case 'membership':
                print(membership(labyrinth, arg))
            case 'equal':
                print(equal_labyrinths(labyrinth, arg))
            case _:
                print('Неизвестная инструкция')

    # На будущее
    # if args.m == 'No' and args.p == 'No':
    #     print(f"Итоговое количество состояний:{len(labyrinth.states)}")
    #     show(labyrinth)
    # elif args.m != 'No' and args.p == 'No':
    #     labyrinth = labyrinth.minify()
    #     show(labyrinth)
    # elif args.m == 'No' and args.p != 'No':
    #     while not check_planarity(labyrinth)[0]:
    #         labyrinth = make_planar(labyrinth)
    #     show(labyrinth)
    # else:
    #     labyrinth = labyrinth.minify()
    #     while not check_planarity(labyrinth)[0]:
    #         labyrinth = make_planar(labyrinth).minify()

