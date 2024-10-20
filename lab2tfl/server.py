from flask import request, jsonify
from app import app
from member_equal import membership, equal_labyrinths
from automata.fa.dfa import DFA


labyrinth: DFA


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
    main_prefixes = data.get('main_prefixes')
    extended_prefixes = data.get('non_main_prefixes')
    suffixes = data.get('suffixes')
    table_str = data.get('table')

    print(main_prefixes, extended_prefixes, suffixes, table_str)

    return jsonify({'response': 'true'}), 200