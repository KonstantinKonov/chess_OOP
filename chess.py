#from colorama import init, Fore
import os
#import curses

###система обозначений фигур

command = 'cls' #for windows

# словарь dict содержит обозначения фигур
# белые  большими буквами, черные - маленькими
d_white_figs = { 'pawn' : 'P', 
                 'rook' : 'R', 
                 'knight' : 'N', # kNight
                 'bishop' : 'B',
                 'queen' : 'Q',
                 'king' : 'K',
                 'Empty' : '.'}

d_black_figs = { 'pawn' : 'p',
                 'rook' : 'r',
                 'knight' : 'n',
                 'bishop' : 'b',
                 'queen' : 'q',
                 'king' : 'k',
                 'Empty' : '.'}

# перевернутый словарь, ключ и значение меняются местами
d_white_code_to_fig = dict( zip(d_white_figs.values(), d_white_figs.keys() ))
d_black_code_to_fig = dict( zip(d_black_figs.values(), d_black_figs.keys() ))

# список с ключами черных фигур ('p', 'r', 'n', 'b', 'q' ...)
blackfigs = list(d_black_code_to_fig.keys())
# удаляем . из этого списка
blackfigs.pop(6)

whitefigs = list(d_white_code_to_fig.keys())
whitefigs.pop(6)

#print('inv', d_black_code_to_fig)

# is_possible_castling_white = True
# is_possible_castling_white = False

# коды типов ходов
walk_types = {
                '0' : 'move',
                '1' : 'capture',
                '2' : 'castling',
                '3' : 'transformation'
}

# коды цветов для отображения доски
WHITE_COLOR = "\033[33m{}"
BLACK_COLOR = "\033[35m{}"
EMPTY_COLOR = "\033[0m{}"
RED_COLOR   = "\033[31m{}"
GREEN_COLOR = "\033[32m{}"

figures = {
            'white' : d_white_figs,
            'black' : d_black_figs}

colors_nums = {
                0 : 'white',
                1 : 'black'
}

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
digits  = ['1', '2', '3', '4', '5', '6', '7', '8']

# делаем двумерный массив из значений (например 'A3') 8x8 - шахматная доска
all_cells = [ let+num for num in digits for let in letters]

moves = []

WhiteBottom = True

def out_yellow(text, end = '\n'):
    print("\033[33m{}".format(text))

def out_viol(text, end = '\n'):
    print("\033[35m{}".format(text))

def out_usual(text, end = '\n'):
    print("\033[0m{}".format(text), end)

# out_yellow('ПРИВЕТ')
# out_viol('ABCD')
# out_usual('Обычный')
# print('asdfa')

def OutputLetters(letters):
    print('  ', end='')
    for i in range(len(letters)):
        print(letters[i], end=' ')
    print('\n')

# ?
##пустые клетки обозначаются нулем

# функция расставляет фигуры по доске (начальная позиция)
def ArrangeFigures( WhiteBottom = True ):
    empty_row    = ['.', '.', '.', '.', '.', '.', '.', '.']
    white_pawns  = ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P']
    white_pieces = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
    black_pawns  = ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p']
    black_pieces = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']

    board = [ empty_row.copy() for i in range(8)]

    if WhiteBottom:
        board[0] = black_pieces.copy()
        board[1] = black_pawns.copy()
        board[6] = white_pawns.copy()
        board[7] = white_pieces.copy()
    else:
        board[7] = black_pieces.copy()
        board[6] = black_pawns.copy()
        board[1] = white_pawns.copy()
        board[0] = white_pieces.copy()

    return board

# функция превращает координаты вида 'E4' в координаты массива (4, 3)
def GetIndexesByCell(string):
    """
    string = 'E4'
    :param string:
    :return:
    """
    letter = string[0]
    num    = int(string[1])
    cell_x = ord(letter) - 64

    i = 8 - num
    j = cell_x - 1

    return i, j

# функция возвращает элемент массива с индексом (x, y), т.е. какая фигура в массиве с индексом (x, y)
def GetFigByIndexes(board, x, y):
    return board[x][y]

# возвращает координаты определенной фигуры(например, пешки), если таких фигур много, возвращает первую найденную, если таки фигур нет, то возвращает (-1, -1)
def SearchFig(board, type, color):
    """
    поиск фигуры на доске
    :param board:
    :param type:
    :param color:
    :return:
    """
    figlet = figures[color][type]

    for i in range(8):
        for j in range(8):
            if board[i][j] == figlet:
                return i,j

    return -1,-1

# (4, 3) -> 'E4'
def GetCellByIndexes(i, j):
    letter = chr(j+65)
    digit = str(8-i)
    return letter+digit

# функция переводит код фигуры, например, 'P' -> (black, 'pawn')
def GetFigInfo(code):
    """
    code - строка
    """
    if code != '.':
        if code in list(d_white_figs.values()):
            color = 'white'
            type = d_white_code_to_fig[code]
        elif code in list(d_black_figs.values()):
            color = 'black'
            type = d_black_code_to_fig[code]
    else:
        color = 'Empty'
        type  = 'Empty'

    return color, type

# поставить фигуру на доску в клетку (например 'p' в 'E4')
def SetFigToCell(board, cell, color, type):
    code = figures[color][type]
    i, j = GetIndexesByCell(cell)
    board[i][j] = code

    return i, j, code

# двигаем фигуру из старой клетки в новую
def MoveFig(board, old_cell, new_cell):
    x, y = GetIndexesByCell(old_cell)
    fig_info = GetFigInfo( GetFigByIndexes(board, x, y) )
    color = fig_info[0]
    type  = fig_info[1]

    SetFigToCell(board, old_cell, 'white', 'Empty')
    SetFigToCell(board, new_cell, color, type)

# возвращает цвет клетки доски
def GetCellColor(cell):
    x,y = GetIndexesByCell(cell)
    s = x + y

    if s % 2 == 1:
        return 'black'
    else:
        return 'white'

# функция печатает доску
def OutputBoard(board):
    print('Доска:\n')

    OutputLetters(letters)

    for i in range(len(board)): #строки
        print(8-i, end = ' ')
        for j in range(len(board[0])):
            if GetFigInfo(board[i][j])[0] == 'white':
                print(WHITE_COLOR.format(board[i][j]), end = ' ')
                print(EMPTY_COLOR.format(''), end='')
            elif GetFigInfo(board[i][j])[0] == 'black':
                print(BLACK_COLOR.format(board[i][j]), end = ' ')
                print(EMPTY_COLOR.format(''), end='')
            else: #GetFigInfo(board[i][j])[0] == 'Empty':
                print(EMPTY_COLOR.format(board[i][j]), end = ' ')

            if j==7:
                print(8-i)
    print('')
    OutputLetters(letters)

# принадлежит ли фигура игроку
def CanTouch(player, cell):
    player_color = colors_nums[player]

    #цвет фигуры находящейся в ячейке:
    x, y = GetIndexesByCell(cell)
    fig_color = GetFigInfo(GetFigByIndexes(board, x, y))[0]

    if player_color != fig_color:
        return False

    return True

# 
def CheckPawnDirectMove(board, old_cell, new_cell):
    """
    проверяет может ли пешка ходить вперед?
    """
    x1, y1 = GetIndexesByCell(old_cell)
    x2, y2 = GetIndexesByCell(new_cell)

    fig_info = GetFigInfo(board[x1][y1])
    color = fig_info[0]
    type  = fig_info[1]

    is_empty = GetFigInfo(board[x2][y2])[1] == 'Empty'

    intermed_res = -1

    # продвижение вперед без учета взятия и en passant
    if color == 'white':
        if CheckExistanceIndexes(x2 + 1, y2):
            is_empty_interm_white = GetFigInfo(board[x2 + 1][y2])[1] == 'Empty'
        else:
            is_empty_interm_white = False

        if x1 == 6:  # если стоит на второй горизонтали
            if (x1 - x2 == 1) and (y1 == y2) and is_empty:# and is_empty_interm_white:
                intermed_res = True
            elif (x1 - x2 == 2) and (y1 == y2) and is_empty and is_empty_interm_white:
                intermed_res = True
            else:
                intermed_res = False
        else:  # пешка уже ходила
            if (x1 - x2 == 1) and (y1 == y2) and is_empty:
                intermed_res = True
            else:
                intermed_res = False
    elif color == 'black':
        if CheckExistanceIndexes(x2 - 1, y2):
            is_empty_interm_black = GetFigInfo(board[x2 - 1][y2])[1] == 'Empty'
        else:
            is_empty_interm_black = False

        if x1 == 1:  # если стоит на второй горизонтали
            if (x2 - x1 == 1) and (y1 == y2) and is_empty:# and is_empty_interm_black:
                intermed_res = True
            elif (x2 - x1 == 2) and (y1 == y2) and is_empty and is_empty_interm_black:
                intermed_res = True
            else:
                intermed_res = False
        else:  # пешка уже ходила
            if (x2 - x1 == 1) and (y1 == y2) and is_empty:
                intermed_res = True
            else:
                intermed_res = False

    return intermed_res

def CheckCapturePawn(board, old_cell, new_cell):
    """
    Проверяет может ли пешка взять фигуру на новом поле
    """
    x1, y1 = GetIndexesByCell(old_cell)
    x2, y2 = GetIndexesByCell(new_cell)

    fig_info = GetFigInfo(board[x1][y1])
    color = fig_info[0]
    type = fig_info[1]

    fig_info2 = GetFigInfo(board[x2][y2])
    color2 = fig_info2[0]
    type2 = fig_info2[1]

    is_not_empty = GetFigInfo(board[x2][y2])[1] != 'Empty'

    intermed_res = -1
    if color == 'white':
        if (x1 - x2 == 1) and (abs(y2-y1) == 1) and is_not_empty and color2 == 'black':
            intermed_res = True
        else:
            intermed_res = False
    elif color == 'black':
        if (x2 - x1 == 1) and (abs(y2-y1) == 1) and is_not_empty and color2 == 'white':
            intermed_res = True
        else:
            intermed_res = False

    return intermed_res

# проверка может ли пешка превратиться в ферзя
def CheckPawnTransformation(board, old_cell, new_cell):
    x1, y1 = GetIndexesByCell(old_cell)
    x2, y2 = GetIndexesByCell(new_cell)

    fig_info = GetFigInfo(board[x1][y1])
    color = fig_info[0]
    type = fig_info[1]
    # return ???


def GetAllFigures(board, color):
    """
    получает список полей, где стоят все фигуры данного цвета

    :param board:
    :param color:
    :return:
    """
    cells = []

    if color == 'white':
        for i in range(8):
            for j in range(8):
                if board[i][j] in whitefigs:
                    cells.append(GetCellByIndexes(i,j))

    elif color == 'black':
        for i in range(8):
            for j in range(8):
                if board[i][j] in blackfigs:
                    cells.append(GetCellByIndexes(i, j))

    return cells

def CheckMovesPawn(board, old_cell, new_cell):
    # x1, y1 = GetIndexesByCell(old_cell)
    # x2, y2 = GetIndexesByCell(new_cell)
    #
    # fig_info = GetFigInfo(board[x1][y1])
    # color = fig_info[0]
    # type  = fig_info[1]
    """
    проверяем может ли пешка ходить
    рокировка, превращение, открытие короля, en passant не проверяем
    """
    res1 = CheckPawnDirectMove(board, old_cell, new_cell)
    res2 = CheckCapturePawn(board, old_cell, new_cell)
    # ???

    return (res1 or res2)


def CheckRookDirectMove(board, old_cell, new_cell):
    """
    проверяет может ли ладья ходить без взятия
    :param board:
    :param old_cell:
    :param new_cell:
    :return:
    """

    x1, y1 = GetIndexesByCell(old_cell)
    x2, y2 = GetIndexesByCell(new_cell)

    res1 = False
    res2 = False

    if (x1 == x2) ^ (y1 == y2):
        res1 = True

        if x1 == x2: #движение по горизонтали
            res2 = True

            if y2 > y1:
                #проверяем от y1+1 до y2 вкл
                for i in range(y1+1, y2+1):
                    res2 = res2 and (GetFigInfo(board[x1][i])[1] == 'Empty')
            elif y2 < y1:
                #проверяем от y2 до y1-1
                for i in range(y2, y1):
                    res2 = res2 and (GetFigInfo(board[x1][i])[1] == 'Empty')
        elif y1 == y2: #движение по вертикали
            res2  = True

            if x2 > x1:
                #проверяем от x1+1 до x2 вкл
                for i in range(x1+1, x2+1):
                    res2 = res2 and (GetFigInfo(board[i][y1])[1] == 'Empty')
            elif x2 < x1:
                #проверяем от y2 до y1-1
                for i in range(x2, x1):
                    res2 = res2 and (GetFigInfo(board[i][y1])[1] == 'Empty')

    return res1 and res2

def CheckCaptureRook(board, old_cell, new_cell):
    """
    проверяет может ли ладья брать фигуру

    :param board:
    :param old_cell:
    :param new_cell:
    :return:
    """
    x1, y1 = GetIndexesByCell(old_cell)
    x2, y2 = GetIndexesByCell(new_cell)

    fig_info = GetFigInfo(board[x1][y1])
    color = fig_info[0]
    type  = fig_info[1]

    fig_info2 = GetFigInfo(board[x2][y2])
    color2 = fig_info2[0]
    type2 = fig_info2[1]

    is_not_empty = GetFigInfo(board[x2][y2])[1] != 'Empty'
    is_diff_colors = (color != color2)

    res = False

    if (x1==x2) and (y1==y2):
        return False

    if y1==y2:
        if x2 > x1: #ходим вниз
            new = new_cell[0] + str(int(new_cell[1])+1)
        elif x2 < x1: #ходим вверх
            new = new_cell[0] + str(int(new_cell[1])-1)
    elif x1==x2: #ходим по горизонтали
        if y2 > y1: #ходим вправо
            new = chr(ord(new_cell[0])-1) + new_cell[1]
        elif y2 < y1: #ходим влево
            new = chr(ord(new_cell[0])+1) + new_cell[1]
    else:
        return res

    if old_cell == new:
        res = True
    else:
        res = CheckRookDirectMove(board, old_cell, new)

    return is_not_empty and is_diff_colors and res

def CheckMovesRook(board, old_cell, new_cell):
    res1 = CheckRookDirectMove(board, old_cell, new_cell)
    res2 = CheckCaptureRook(board, old_cell, new_cell)

    return res1 or res2

def CheckKnightDirectMove(board, old_cell, new_cell):
    x1, y1 = GetIndexesByCell(old_cell)
    x2, y2 = GetIndexesByCell(new_cell)

    is_empty = GetFigInfo(board[x2][y2])[1] == 'Empty'

    fig_info = GetFigInfo(board[x1][y1])
    color = fig_info[0]
    type = fig_info[1]

    fig_info2 = GetFigInfo(board[x2][y2])
    color2 = fig_info2[0]
    type2 = fig_info2[1]
    diff_colors = color != color2

    if ((abs(x2-x1)==2 and abs(y2-y1)==1) or (abs(x2-x1)==1 and abs(y2-y1)==2)) and (is_empty or diff_colors):
        return True

    return False

def CheckCaptureKnight(board, old_cell, new_cell):
    x1, y1 = GetIndexesByCell(old_cell)
    x2, y2 = GetIndexesByCell(new_cell)

    is_not_empty = GetFigInfo(board[x2][y2])[1] != 'Empty'

    fig_info = GetFigInfo(board[x1][y1])
    color = fig_info[0]
    type = fig_info[1]

    fig_info2 = GetFigInfo(board[x2][y2])
    color2 = fig_info2[0]
    type2 = fig_info2[1]

    diff_colors = color != color2

    if ((abs(x2-x1)==2 and abs(y2-y1)==1) or (abs(x2-x1)==1 and abs(y2-y1)==2)) and (is_not_empty and diff_colors):
        return True

    return False

def CheckMovesKnight(board, old_cell, new_cell):
    res1 = CheckKnightDirectMove(board, old_cell, new_cell)
    res2 = CheckCaptureKnight(board, old_cell, new_cell)

    return res1 or res2

def CheckBishopDirectMove(board, old_cell, new_cell):
    x1, y1 = GetIndexesByCell(old_cell)
    x2, y2 = GetIndexesByCell(new_cell)

    res1 = False
    res2 = False

    if abs(x1-x2) == abs(y1-y2):
        res1 = True

        delta_x = abs(x1 - x2)
        delta_y = abs(y1 - y2)
        N = min(delta_x, delta_y)

        x = x1
        y = y1

        if x2<x1 and y2<y1:
            res2 = True

            for i in range(1, N+1):
                x = x-i
                y = y-i
                res2 = res2 and (GetFigInfo(board[x][y])[1] == 'Empty')

        elif x2<x1 and y2>y1:
            res2 = True

            for i in range(1, N + 1):
                x = x - i
                y = y + i
                res2 = res2 and (GetFigInfo(board[x][y])[1] == 'Empty')

        elif x2>x1 and y2<y1:
            res2 = True

            for i in range(1, N + 1):
                x = x + i
                y = y - i
                res2 = res2 and (GetFigInfo(board[x][y])[1] == 'Empty')

        elif x2>x1 and y2>y1:
            res2 = True

            for i in range(1, N + 1):
                x = x + i
                y = y + i
                res2 = res2 and (GetFigInfo(board[x][y])[1] == 'Empty')

    return res1 and res2

def CheckCaptureBishop(board, old_cell, new_cell):
    """
    проверяет может ли ладья брать фигуру

    :param board:
    :param old_cell:
    :param new_cell:
    :return:
    """
    x1, y1 = GetIndexesByCell(old_cell)
    x2, y2 = GetIndexesByCell(new_cell)

    fig_info = GetFigInfo(board[x1][y1])
    color = fig_info[0]
    type  = fig_info[1]

    fig_info2 = GetFigInfo(board[x2][y2])
    color2 = fig_info2[0]
    type2 = fig_info2[1]

    is_not_empty = GetFigInfo(board[x2][y2])[1] != 'Empty'
    is_diff_colors = color != color2

    res = False

    if (x1==x2) or (y1==y2):
        return False

    if x1>x2 and y1>y2:
        new = chr( ord(new_cell[0])  + 1) + str(int(new_cell[1]) - 1)
    elif x1>x2 and y1<y2:
        new = chr( ord(new_cell[0])  - 1) + str(int(new_cell[1]) - 1)
    elif x1<x2 and y1>y2:
        new = chr( ord(new_cell[0])  + 1) + str(int(new_cell[1]) + 1)
    elif x1<x2 and y1<y2:
        new = chr( ord(new_cell[0])  - 1) + str(int(new_cell[1]) + 1)

    if new != old_cell:
        res = CheckBishopDirectMove(board, old_cell, new)
    else:
        res = True

    return is_not_empty and is_diff_colors and res

def CheckMovesBishop(board, old_cell, new_cell):
    res1 = CheckBishopDirectMove(board, old_cell, new_cell)
    res2 = CheckCaptureBishop(board, old_cell, new_cell)

    return res1 or res2

def CheckQueenDirectMove(board, old_cell, new_cell):
    res1 = CheckRookDirectMove(board, old_cell, new_cell)
    res2 = CheckBishopDirectMove(board, old_cell, new_cell)

    return res1 or res2

def CheckCaptureQueen(board, old_cell, new_cell):
    res1 = CheckCaptureRook(board, old_cell, new_cell)
    res2 = CheckCaptureBishop(board, old_cell, new_cell)

    return res1 or res2

def CheckMovesQueen(board, old_cell, new_cell):
    res1 = CheckQueenDirectMove(board, old_cell, new_cell)
    res2 = CheckCaptureQueen(board, old_cell, new_cell)
    return res1 or res2

def CheckKingDirectMove(board, old_cell, new_cell):
    x1, y1 = GetIndexesByCell(old_cell)
    x2, y2 = GetIndexesByCell(new_cell)

    fig_info = GetFigInfo(board[x1][y1])
    color = fig_info[0]
    type = fig_info[1]

    fig_info2 = GetFigInfo(board[x2][y2])
    color2 = fig_info2[0]
    type2 = fig_info2[1]

    is_empty = GetFigInfo(board[x2][y2])[1] == 'Empty'
    #is_diff_colors = color != color2

    if (abs(x2-x1)==1 or abs(y2-y1)==1) and is_empty:
        res = True
    else:
        res = False

    #res2 - описывает приближение королей
    if  color == 'white':
        opposite_color = 'black'
        fig = 'k'
    elif color == 'black':
        opposite_color = 'white'
        fig = 'K'

    i,j = SearchFig(board, 'king', opposite_color)
    enemy_king_cell = GetCellByIndexes(i, j)
    x,y = GetIndexesByCell(enemy_king_cell)

    if ((abs(y2-y)==1) and (abs(x2-x)<=1)) or ((abs(x2-x)==1) and (abs(y2-y)<=1)):
        res2 = False
    else:
        res2 = True

    return res & res2

def CheckCaptureKing(board, old_cell, new_cell):
    x1, y1 = GetIndexesByCell(old_cell)
    x2, y2 = GetIndexesByCell(new_cell)

    fig_info = GetFigInfo(board[x1][y1])
    color = fig_info[0]
    type = fig_info[1]

    fig_info2 = GetFigInfo(board[x2][y2])
    color2 = fig_info2[0]
    type2 = fig_info2[1]

    is_not_empty = GetFigInfo(board[x2][y2])[1] != 'Empty'
    is_diff_colors = color != color2
    is_not_enemy_king = type2 != 'king'

    res = False
    if (abs(x2 - x1) == 1 or abs(y2 - y1) == 1) and is_not_empty and is_diff_colors and is_not_enemy_king:
        return True
    else:
        return False

def CheckMovesKing(board, old_cell, new_cell):
    res1 = CheckKingDirectMove(board, old_cell, new_cell)
    res2 = CheckCaptureKing(board, old_cell, new_cell)
    return res1 or res2

# функция проверяет корректность координат клетки, т.е. если ввести 'L9' - то вернет False
def CheckExistanceCell(cell):
    """
    E4
    :param cell:
    :return:
    """
    letter = ord(cell[0])
    num = int(cell[1])

    if (num < 1) or (num > 8):
        return False

    if (letter < 65) or (letter > 72): #поддержка только больших букв
        return False

    return True

# функция проверяет корректность коодинат (2, 3) -> True, (8, 9) -> False
def CheckExistanceIndexes(i,j):
    if (i<0) or (i>7):
        return False

    if (j<0) or (j>7):
        return False

    return True

def IsCheck(board, color):
    if color == 'white':
        lst_black = GetAllFigures(board, 'black')
        white_king = SearchFig(board, 'king', 'white') #выдает индексы на доске
        i = white_king[0]
        j = white_king[1]

        white_king_cell = GetCellByIndexes(i, j)
        res = False

        for f in lst_black:
            x, y = GetIndexesByCell(f)

            fig_info = GetFigInfo(board[x][y])
            type = fig_info[1]

            if type == 'pawn':
                res = CheckCapturePawn(board, f, white_king_cell)
                if res:
                    return True
            elif type == 'rook':
                res = CheckCaptureRook(board, f, white_king_cell)
                if res:
                    return True
            elif type == 'knight':
                res = CheckCaptureKnight(board, f, white_king_cell)
                if res:
                    return True
            elif type == 'bishop':
                res = CheckCaptureBishop(board, f, white_king_cell)
                if res:
                    return True
            elif type == 'queen':
                res = CheckCaptureQueen(board, f, white_king_cell)
                if res:
                    return True

        return False
    elif color == 'black':
        lst_white = GetAllFigures(board, 'white')
        black_king = SearchFig(board, 'king', 'black')  # выдает индексы на доске
        i = black_king[0]
        j = black_king[1]

        black_king_cell = GetCellByIndexes(i, j)
        res = False

        for f in lst_white:
            x, y = GetIndexesByCell(f)

            fig_info = GetFigInfo(board[x][y])
            type = fig_info[1]

            if type == 'pawn':
                res = CheckCapturePawn(board, f, black_king_cell)
                if res:
                    return True
            elif type == 'rook':
                res = CheckCaptureRook(board, f, black_king_cell)
                if res:
                    return True
            elif type == 'knight':
                res = CheckCaptureKnight(board, f, black_king_cell)
                if res:
                    return True
            elif type == 'bishop':
                res = CheckCaptureBishop(board, f, black_king_cell)
                if res:
                    return True
            elif type == 'queen':
                res = CheckCaptureQueen(board, f, black_king_cell)
                if res:
                    return True

        return False

# функция осуществляет обмен пешки на ферзя
def PawnTransformation(board, color, end_cell, WhiteBottom=True):
    if color=='white' and ( ( end_cell[1]=='8' and WhiteBottom ) or
                            ( end_cell[1]=='1' and not WhiteBottom ) ):
        print(f"You have reached transformation field! Choose one of the following fig type: { whitefigs[1:] }")
        new_fig_code = input()

        while new_fig_code not in whitefigs[1:]:
            print(f"Choose one of the following fig type: {whitefigs[1:]}")
            new_fig_code = input()

        # i,j = GetIndexesByCell(end_cell)
        # board[i][j] = new_fig_code

        return new_fig_code

    elif color=='black' and ( ( end_cell[1]=='1' and WhiteBottom ) or
                            ( end_cell[1]=='8' and not WhiteBottom ) ):
        print(f"You have reached transformation field! Choose one of the following fig type: {blackfigs[1:]}")
        new_fig_code = input()

        while new_fig_code not in blackfigs[1:]:
            print(f"Choose one of the following fig type: {blackfigs[1:]}")
            new_fig_code = input()

        # i, j = GetIndexesByCell(end_cell)
        # board[i][j] = new_fig_code

        return new_fig_code

    return -1

def WhereAllowedToGo(board, start_cell):
    """
    вычиляет, куда можно ходить с поля start_cell
    """
    x, y = GetIndexesByCell(start_cell)

    fig_info = GetFigInfo(board[x][y])
    color = fig_info[0]
    type = fig_info[1]
    lst_walks = []

    if type == 'pawn':
        checker_func = CheckMovesPawn
    elif type == 'rook':
        checker_func = CheckMovesRook
    elif type == 'knight':
        checker_func = CheckMovesKnight
    elif type == 'bishop':
        checker_func = CheckMovesBishop
    elif type == 'queen':
        checker_func = CheckMovesQueen
    elif type == 'king':
        checker_func = CheckMovesKing

    for cell in all_cells:
        if (start_cell != cell) and checker_func(board, start_cell, cell):
            lst_walks.append(cell)

    return lst_walks

if __name__ == '__main__':
    board = ArrangeFigures(WhiteBottom)

    # в windows очищает экран комманда 'cls'
    os.system(command)
    OutputBoard(board)

    player = 0 #player 0 ходит белыми, а player 1 ходит черными

    game = True #признак продолжения игры
    c = 0

    # x,y = GetIndexesByCell('E4')
    # print('info:', GetFigInfo(GetFigByIndexes(board, x, y))[0])

    ###Исходная расстановка фигур для тестов, можно закоментировать эти строки и тогда будет расстановка с начала игры
    board = [['r', 'n', 'b', 'q', 'k', 'b', '.', 'r'],
            ['p' ,'p', 'p', 'p', 'p', 'p', 'P', 'p'],
            ['.', '.', '.', 'q', '.', '.', '.', '.' ],
            ['.', '.', '.', '.', 'K', '.', '.', '.' ],
            ['p', '.', '.', '.', '.', '.', '.', '.' ],
            ['.', 'N', '.', '.', '.', '.', '.', '.' ],
            ['P', 'P', 'p', 'P', '.', 'P', 'P', 'P' ],
            ['R', 'B', '.', 'Q', '.', 'B', 'N', 'R' ]]

    board_for_check = board.copy()

    os.system(command)
    OutputBoard(board)

    MAX_MOVES = 10

    #сделать горячие клавиши - выход, ход назад и ход вперед

    while game:
        print(f'Player {player} make your move...')
        OutputBoard(board)
        print('Enter start cell:')
        start_cell = input()
        touch = CanTouch(player, start_cell)
        transformation = -1

        if touch == False:
            print("ERROR: You can't move by figure of your opponent or You should choose your figure! Please make right move!")
            continue

        #проверка куда может ходить фигура
        # lst_walks = WhereAllowedToGo(board, start_cell)
        # print("You can go to:\n", lst_walks)

        print('Enter end cell:')
        end_cell = input()

        x1, y1 = GetIndexesByCell(start_cell)
        fig_info = GetFigInfo(board[x1][y1])

        x2, y2 = GetIndexesByCell(end_cell)
        if not CheckExistanceIndexes(x2, y2):
            print("ERROR: Incorrect final cell!")
            continue

        color = fig_info[0]
        type = fig_info[1]

        if color=='white':
            opponent_color = 'black'
        elif color=='black':
            opponent_color = 'white'
        else:
            opponent_color = 'Error'

        if type == 'pawn':
            if CheckMovesPawn(board, start_cell, end_cell) == False:
                print("pawn can't go this way!")
                continue
            else:
                if end_cell[1] == '1' or end_cell[1] == '8':
                    transformation = PawnTransformation(board, color, end_cell, WhiteBottom)

        elif type == 'rook':
            if CheckMovesRook(board, start_cell, end_cell) == False:
                print("rook can't go this way!")
                continue
        elif type == 'knight':
            if CheckMovesKnight(board, start_cell, end_cell) == False:
                print("knight can't go this way!")
                continue
        elif type == 'bishop':
            if CheckMovesBishop(board, start_cell, end_cell) == False:
                print("bishop can't go this way!")
                continue
        elif type == 'queen':
            if CheckMovesQueen(board, start_cell, end_cell) == False:
                print("queen can't go this way!")
                continue
        elif type == 'king':
            if CheckMovesKing(board, start_cell, end_cell) == False:
                print("king can't go this way!")
                continue

        MoveFig(board_for_check, start_cell, end_cell)
        if transformation != -1:
            # i,j = GetIndexesByCell(end_cell)
            board_for_check[x2][y2] = transformation

        is_check_currect_player = IsCheck(board_for_check, color)
        if is_check_currect_player:
            print("You king is opened for attack or checked! You should defend your king!")
            board_for_check = board.copy()
            continue
        else:
            board = board_for_check.copy()

        moves.append( [start_cell, end_cell] )

        os.system(command)

        ###Проверка что игрок ходит своими фигурами или бъет фигуры оппонента
        OutputBoard(board)

        if IsCheck(board, opponent_color):
            print(RED_COLOR.format(f"CHECK for {opponent_color} king!"))
            print(EMPTY_COLOR.format(''), end='')

        player += 1
        player = player % 2

        c+=1
        if c > MAX_MOVES:
            break