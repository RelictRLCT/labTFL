from flask import request, jsonify
from app import app
from lab2tfl.dfa_from_table import make_dfa_from_table
from member_equal import membership, equal_labyrinths
from automata.fa.dfa import DFA
from show import show

labyrinth: DFA


def process_table(main_prefixes_raw: str, extended_prefixes_raw: str, suffixes_raw: str, table_str: str) -> DFA:

    def process_items(items_raw):
        items = items_raw.strip().split()
        if not items:
            return ['ε']
        processed = []
        for item in items:
            if item == '' or item == 'ε':
                processed.append('ε')
            else:
                if item.startswith('ε') and item != 'ε':
                    item = item[1:]
                processed.append(item)
        return processed

    main_prefixes = process_items(main_prefixes_raw)
    extended_prefixes = process_items(extended_prefixes_raw)
    suffixes = process_items(suffixes_raw)

    prefixes = main_prefixes + extended_prefixes

    # Удаляем пробелы из строки таблицы
    table_values = list(table_str.replace(' ', ''))
    print(table_values)
    # Убедимся, что количество значений в table_values соответствует количеству комбинаций
    total_combinations = len(prefixes) * len(suffixes)
    if len(table_values) < total_combinations:
        # Дополняем недостающие значения дефолтным '-'
        table_values += ['-'] * (total_combinations - len(table_values))

    # Заполняем таблицу
    table = {}
    idx = 0
    for prefix in prefixes:
        for suffix in suffixes:
            value = table_values[idx]
            idx += 1
            table[(prefix, suffix)] = value

    print(main_prefixes, extended_prefixes, suffixes, table)

    return make_dfa_from_table(main_prefixes, extended_prefixes, suffixes, table)

    # Здесь вы можете продолжить логику с использованием main_prefixes, extended_prefixes, suffixes и table


# Функция для установки лабиринта из main.py
def set_labyrinth(new_labyrinth):
    global labyrinth
    labyrinth = new_labyrinth


@app.route('/checkWord', methods=['POST'])
def check_word():
    # Извлечение данных из запроса
    data = request.get_json()
    word = data.get('word')

    if not word:
        return jsonify({'error': 'ГДЕ СЛОВО????'}), 400

    # Проверка, принадлежит ли слово языку
    if membership(labyrinth, word):
        return jsonify({'response': '1'}), 200
    else:
        return jsonify({'response': '0'}), 200


@app.route('/checkTable', methods=['POST'])
def check_table():
    data = request.get_json()
    main_prefixes_raw = data.get('main_prefixes', '')
    extended_prefixes_raw = data.get('non_main_prefixes', '')
    suffixes_raw = data.get('suffixes', '')
    table_str = data.get('table', '')

    user_dfa = process_table(main_prefixes_raw, extended_prefixes_raw, suffixes_raw, table_str)

    resp = equal_labyrinths(labyrinth, user_dfa)

    show(user_dfa, 'user_labyrinth.png')

    if resp == 'true':
        show(user_dfa, 'user_labyrinth.png')

    print(f'ОТВЕТ {resp}')
    return jsonify({'response': resp}), 200