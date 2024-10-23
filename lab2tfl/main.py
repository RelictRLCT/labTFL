from generator import generate_labyrinth
from planarity import check_planarity
from show import show
import argparse
from app import app
import server


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Генератор планарного лабиринта')
    parser.add_argument('-p', type=str, default='No', help='Выполнить планаризацию (-p yes)')
    args = parser.parse_args()

    labyrinth = generate_labyrinth(plan=args.p)

    print(f"Количество состояний: {len(labyrinth.states)}")
    check_planarity(labyrinth)
    show(labyrinth)

    server.set_labyrinth(labyrinth)
    app.run('0.0.0.0', 8095)
