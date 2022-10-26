# Проверка из семинара 5 (немного модернизирована)
# Проверка на строку, столбец, главную диагональ, второстепенную диагональ. на выходе список координат
from random import randint


def check_winner(matrix):
    """
    Проверка строк, столбцов, диагоналей
    :param matrix:
    :return: list
    """
    var_win = []
    # варианты победы
    for i in range(3):
        if matrix[i][0]['text'] == matrix[i][1]['text'] == matrix[i][2]['text'] != '':
            var_win = [i, 0, i, 1, i, 2]
        if matrix[0][i]['text'] == matrix[1][i]['text'] == matrix[2][i]['text'] != '':
            var_win = [0, i, 1, i, 2, i]
    if matrix[0][0]['text'] == matrix[1][1]['text'] == matrix[2][2]['text'] != '':
        var_win = [0, 0, 1, 1, 2, 2]
    if matrix[0][2]['text'] == matrix[1][1]['text'] == matrix[2][0]['text'] != '':
        var_win = [0, 2, 1, 1, 2, 0]
    return var_win


# определение координаты хода IQ AI
def iq_move(matrix):
    win_lines = {
        0: ((0, 0), (0, 1), (0, 2)),
        1: ((1, 0), (1, 1), (1, 2)),
        2: ((2, 0), (2, 1), (2, 2)),
        3: ((0, 0), (1, 0), (2, 0)),
        4: ((0, 1), (1, 1), (2, 1)),
        5: ((0, 2), (1, 2), (2, 2)),
        6: ((0, 0), (1, 1), (2, 2)),
        7: ((0, 2), (1, 1), (2, 0)),
    }
    # если центр не занят, ставим туда
    if matrix[1][1]['text'] == '':
        return [1, 1]
    # вариант, чтобы человек мог сыграть только вничью или проиграть - занять центр первым ходом и один из углов вторым ходом
    line_two_0 = -1
    for line in win_lines.keys():
        count_X = 0
        count_0 = 0
        for cell in win_lines[line]:
            if matrix[cell[0]][cell[1]]['text'] == 'X':
                count_X += 1
            elif matrix[cell[0]][cell[1]]['text'] == '0':
                count_0 += 1
        if count_X == 2 and count_0 == 0:
            row, col = find_empty_cell(win_lines[line], matrix)
            return [row, col]
        elif count_0 == 2 and count_X == 0:
            line_two_0 = line
    if line_two_0 != -1:
        row, col = find_empty_cell(win_lines[line_two_0], matrix)
        return [row, col]
    else:
        while True:
            row = randint(0, 2)
            col = randint(0, 2)
            # если поле свободно, ставим маркер бота
            if matrix[row][col]['text'] == '':
                return [row, col]


# нахождение пустой ячейки в линии
def find_empty_cell(line, matrix):
    for cell in line:
        if matrix[cell[0]][cell[1]]['text'] == '':
            return [cell[0], cell[1]]
