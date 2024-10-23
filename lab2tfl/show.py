from automata.fa.dfa import DFA
from automata.fa.nfa import NFA
from matplotlib import pyplot as plt
from typing import Union
from pathlib import Path
import os
import shutil

# Глобальная переменная для подсчёта попыток
attempt_counter = 0


def reset_attempt_counter():
    global attempt_counter
    attempt_counter = 0


def create_folder(folder_path):
    Path(folder_path).mkdir(parents=True, exist_ok=True)


def remove_folder(folder_path):
    try:
        shutil.rmtree(folder_path)
        # print(f"Папка {folder_path} удалена.")
    except Exception as e:
        print(f"Ошибка удаления {folder_path}: {e}")


def clear_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Удаляем файл или символическую ссылку
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Удаляем папку и все её содержимое
        except Exception as e:
            print(f"Ошибка при удалении {file_path}: {e}")
    remove_folder(folder_path)


def show(automata: Union[DFA, NFA], is_attempt=False):
    global attempt_counter

    # Создаём папку для изображений, если она не существует
    images_folder = Path("../images")
    create_folder(images_folder)

    if is_attempt:
        attempt_counter += 1

        # Сохранение попытки пользователя
        attempt_folder = images_folder / "attempts"
        create_folder(attempt_folder)
        image_path = attempt_folder / f"attempt_{attempt_counter}.png"

    else:
        # Сохранение исходного лабиринта
        image_path = images_folder / "labyrinth.png"

    automata.show_diagram().draw(str(image_path), prog='dot')
