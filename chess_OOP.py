import os

class Board:
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    digits  = ['1', '2', '3', '4', '5', '6', '7', '8']


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

    figures = {
                'white' : d_white_figs,
                'black' : d_black_figs}

    colors_nums = {
                    0 : 'white',
                    1 : 'black'
    }
    # перевернутый словарь, ключ и значение меняются местами
    d_white_code_to_fig = dict( zip(d_white_figs.values(), d_white_figs.keys() ))
    d_black_code_to_fig = dict( zip(d_black_figs.values(), d_black_figs.keys() ))

    # список с ключами черных фигур ('p', 'r', 'n', 'b', 'q' ...)
    blackfigs = list(d_black_code_to_fig.keys())
    # удаляем . из этого списка
    blackfigs.pop(6)

    whitefigs = list(d_white_code_to_fig.keys())
    whitefigs.pop(6)

    # коды типов ходов
    walk_types = {
                    '0' : 'move',
                    '1' : 'capture',
                    '2' : 'castling',
                    '3' : 'transformation'
    }
    WHITE_COLOR = "\033[33m{}"
    BLACK_COLOR = "\033[35m{}"
    EMPTY_COLOR = "\033[0m{}"
    RED_COLOR   = "\033[31m{}"
    GREEN_COLOR = "\033[32m{}"
    
    empty_row    = ['.', '.', '.', '.', '.', '.', '.', '.']

    def __init__(self):
        self.board = [ self.empty_row.copy() for i in range(8)]

    def arrange_figures(self, white_bottom=True):
        empty_row    = ['.', '.', '.', '.', '.', '.', '.', '.']
        white_pawns  = ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P']
        white_pieces = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        black_pawns  = ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p']
        black_pieces = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']


        if white_bottom:
            self.board[0] = black_pieces.copy()
            self.board[1] = black_pawns.copy()
            self.board[6] = white_pawns.copy()
            self.board[7] = white_pieces.copy()
        else:
            self.board[7] = black_pieces.copy()
            self.board[6] = black_pawns.copy()
            self.board[1] = white_pawns.copy()
            self.board[0] = white_pieces.copy()

        return self.board
    
    def output_letters(self):
        print('  ', end='')
        for i in range(len(self.letters)):
            print(self.letters[i], end=' ')
        print('\n')

    def get_fig_info(self, code):
        """
        code - строка
        """
        if code != '.':
            if code in list(self.d_white_figs.values()):
                color = 'white'
                type = self.d_white_code_to_fig[code]
            elif code in list(self.d_black_figs.values()):
                color = 'black'
                type = self.d_black_code_to_fig[code]
        else:
            color = 'Empty'
            type  = 'Empty'

        return color, type

    # функция печатает доску
    def output_board(self):
        print('Доска:\n')

        self.output_letters()

        for i in range(len(self.board)): #строки
            print(8-i, end = ' ')
            for j in range(len(self.board[0])):
                if self.get_fig_info(self.board[i][j])[0] == 'white':
                    print(self.WHITE_COLOR.format(self.board[i][j]), end = ' ')
                    print(self.EMPTY_COLOR.format(''), end='')
                elif self.get_fig_info(self.board[i][j])[0] == 'black':
                    print(self.BLACK_COLOR.format(self.board[i][j]), end = ' ')
                    print(self.EMPTY_COLOR.format(''), end='')
                else: #GetFigInfo(board[i][j])[0] == 'Empty':
                    print(self.EMPTY_COLOR.format(self.board[i][j]), end = ' ')

                if j==7:
                    print(8-i)
        print('')
        self.output_letters()

    def get_indexes_by_cell(self, s):
        """
        string = 'E4'
        :param string:
        :return:
        """
        letter = s[0]
        num    = int(s[1])
        cell_x = ord(letter) - 64

        i = 8 - num
        j = cell_x - 1

        return i, j

    def get_fig_by_indexes(self, x, y):
        return self.board[x][y]

    def search_fig(self, type, color):
        """
        поиск фигуры на доске
        :param board:
        :param type:
        :param color:
        :return:
        """
        figlet = self.figures[color][type]

        for i in range(8):
            for j in range(8):
                if self.board[i][j] == figlet:
                    return i,j

        return -1,-1

    # (4, 3) -> 'E4'
    def get_cell_by_indexes(self, i, j):
        letter = chr(j+65)
        digit = str(8-i)
        return letter+digit

    # принадлежит ли фигура игроку
    def can_touch(self, player, cell):
        player_color = self.colors_nums[player]

        #цвет фигуры находящейся в ячейке:
        x, y = self.get_indexes_by_cell(cell)
        fig_color = self.get_fig_info(self.get_fig_by_indexes(x, y))[0]

        if player_color != fig_color:
            return False

        return True

    # функция проверяет корректность коодинат (2, 3) -> True, (8, 9) -> False
    def check_existance_indexes(self, i, j):
        if (i<0) or (i>7):
            return False

        if (j<0) or (j>7):
            return False

        return True
    
    # функция переводит код фигуры, например, 'P' -> (black, 'pawn')
    def get_fig_info(self, code):
        """
        code - строка
        """
        if code != '.':
            if code in list(self.d_white_figs.values()):
                color = 'white'
                type = self.d_white_code_to_fig[code]
            elif code in list(self.d_black_figs.values()):
                color = 'black'
                type = self.d_black_code_to_fig[code]
        else:
            color = 'Empty'
            type  = 'Empty'

        return color, type

    # поставить фигуру на доску в клетку (например 'p' в 'E4')
    def set_fig_to_cell(self, cell, color, type):
        code = self.figures[color][type]
        i, j = self.get_indexes_by_cell(cell)
        self.board[i][j] = code

        return i, j, code
    
    def get_all_figures(self, color):
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
                    if self.board[i][j] in self.whitefigs:
                        cells.append(self.get_cell_by_indexes(i,j))

        elif color == 'black':
            for i in range(8):
                for j in range(8):
                    if self.board[i][j] in self.blackfigs:
                        cells.append(self.get_cell_by_indexes(i, j))

        return cells

    def get_cell_color(self, cell):
        x,y = self.get_indexes_by_cell(cell)
        s = x + y

        if s % 2 == 1:
            return 'black'
        else:
            return 'white'

    def move_fig(self, old_cell, new_cell):
        x, y = self.get_indexes_by_cell(old_cell)
        fig_info = self.get_fig_info(self.get_fig_by_indexes(x, y) )
        color = fig_info[0]
        type  = fig_info[1]

        self.set_fig_to_cell(old_cell, 'white', 'Empty')
        self.set_fig_to_cell(new_cell, color, type)

    # функция проверяет корректность координат клетки, т.е. если ввести 'L9' - то вернет False
    def check_existance_cell(self, cell):
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
    def check_existance_indexes(self, i,j):
        if (i<0) or (i>7):
            return False

        if (j<0) or (j>7):
            return False

        return True

    def is_check(self, color):
        if color == 'white':
            lst_black = self.get_all_figures('black')
            white_king = self.search_fig('king', 'white') #выдает индексы на доске
            i = white_king[0]
            j = white_king[1]

            white_king_cell = self.get_cell_by_indexes(i, j)
            res = False

            for f in lst_black:
                x, y = self.get_indexes_by_cell(f)

                fig_info = self.get_fig_info(self.board[x][y])
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



class Figure:
    def __init__(self, color, cell):
        self.color = color
        self.cell = cell


class Pawn(Figure):
    def __init__(self, color, cell):
        super().__init__(color, cell)
    
    def check_pawn_direct_move(self, board, old_cell, new_cell):
        """
        проверяет может ли пешка ходить вперед?
        """
        x1, y1 = board.get_indexes_by_cell(old_cell)
        x2, y2 = board.get_indexes_by_cell(new_cell)

        fig_info = board.get_fig_info(board.get_fig_by_indexes(x1, y1))
        color = fig_info[0]
        type  = fig_info[1]

        is_empty = board.get_fig_info(board.get_fig_by_indexes(x2, y2))[1] == 'Empty'

        intermed_res = -1

        # продвижение вперед без учета взятия и en passant
        if color == 'white':
            if board.check_existance_indexes(x2 + 1, y2):
                is_empty_interm_white = board.get_fig_info(board.get_fig_by_indexes(x2 + 1, y2))[1] == 'Empty'
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
            if board.check_existance_indexes(x2 - 1, y2):
                is_empty_interm_black = board.get_fig_info(board.get_fig_by_indexes(x2 - 1, y2))[1] == 'Empty'
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

    def check_capture_pawn(self, board: Board, old_cell, new_cell):
        """
        Проверяет может ли пешка взять фигуру на новом поле
        """
        x1, y1 = board.get_indexes_by_cell(old_cell)
        x2, y2 = board.get_indexes_by_cell(new_cell)

        fig_info = board.get_fig_info(board.board[x1][y1])
        color = fig_info[0]
        type = fig_info[1]

        fig_info2 = board.get_fig_info(board.board[x2][y2])
        color2 = fig_info2[0]
        type2 = fig_info2[1]

        is_not_empty = board.get_fig_info(board.board[x2][y2])[1] != 'Empty'

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
    def check_pawn_transformation(self, board: Board, old_cell, new_cell):
        x1, y1 = board.get_indexes_by_cell(old_cell)
        x2, y2 = board.get_indexes_by_cell(new_cell)

        fig_info = board.get_fig_info(board.board[x1][y1])
        color = fig_info[0]
        type = fig_info[1]
        # return ???

    def check_moves_pawn(self, board: Board, old_cell, new_cell):
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
        res1 = self.check_pawn_direct_move(board, old_cell, new_cell)
        res2 = self.check_capture_pawn(board, old_cell, new_cell)
        # ???

        return (res1 or res2)


class Rook(Figure):
    def __init__(self, color, cell):
        super().__init__(color, cell)
    
    def check_rook_direct_move(self, board: Board, old_cell, new_cell):
        """
        проверяет может ли ладья ходить без взятия
        :param board:
        :param old_cell:
        :param new_cell:
        :return:
        """

        x1, y1 = board.get_indexes_by_cell(old_cell)
        x2, y2 = board.get_indexes_by_cell(new_cell)

        res1 = False
        res2 = False

        if (x1 == x2) ^ (y1 == y2):
            res1 = True

            if x1 == x2: #движение по горизонтали
                res2 = True

                if y2 > y1:
                    #проверяем от y1+1 до y2 вкл
                    for i in range(y1+1, y2+1):
                        res2 = res2 and (board.get_fig_info(board.board[x1][i])[1] == 'Empty')
                elif y2 < y1:
                    #проверяем от y2 до y1-1
                    for i in range(y2, y1):
                        res2 = res2 and (board.get_fig_info(board.board[x1][i])[1] == 'Empty')
            elif y1 == y2: #движение по вертикали
                res2  = True

                if x2 > x1:
                    #проверяем от x1+1 до x2 вкл
                    for i in range(x1+1, x2+1):
                        res2 = res2 and (board.get_fig_info(board.board[i][y1])[1] == 'Empty')
                elif x2 < x1:
                    #проверяем от y2 до y1-1
                    for i in range(x2, x1):
                        res2 = res2 and (board.get_fig_info(board.board[i][y1])[1] == 'Empty')

        return res1 and res2

    def check_capture_rook(self, board: Board, old_cell, new_cell):
        """
        проверяет может ли ладья брать фигуру

        :param board:
        :param old_cell:
        :param new_cell:
        :return:
        """
        x1, y1 = board.get_indexes_by_cell(old_cell)
        x2, y2 = board.get_indexes_by_cell(new_cell)

        fig_info = board.get_fig_info(board.board[x1][y1])
        color = fig_info[0]
        type  = fig_info[1]

        fig_info2 = board.get_fig_info(board.board[x2][y2])
        color2 = fig_info2[0]
        type2 = fig_info2[1]

        is_not_empty = board.get_fig_info(board.board[x2][y2])[1] != 'Empty'
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
            res = self.check_rook_direct_move(board, old_cell, new)

        return is_not_empty and is_diff_colors and res

    def check_moves_rook(self, board: Board, old_cell, new_cell):
        res1 = self.check_rook_direct_move(board, old_cell, new_cell)
        res2 = self.check_capture_rook(board, old_cell, new_cell)

        return res1 or res2


class Knight(Figure):
    def __init__(self, color, cell):
        super().__init__(color, cell)

    def check_knight_direct_move(self, board: Board, old_cell, new_cell):
        x1, y1 = board.get_indexes_by_cell(old_cell)
        x2, y2 = board.get_indexes_by_cell(new_cell)

        is_empty = board.get_fig_info(board.board[x2][y2])[1] == 'Empty'

        fig_info = board.get_fig_info(board.board[x1][y1])
        color = fig_info[0]
        type = fig_info[1]

        fig_info2 = board.get_fig_info(board.board[x2][y2])
        color2 = fig_info2[0]
        type2 = fig_info2[1]
        diff_colors = color != color2

        if ((abs(x2-x1)==2 and abs(y2-y1)==1) or (abs(x2-x1)==1 and abs(y2-y1)==2)) and (is_empty or diff_colors):
            return True

        return False

    def check_capture_knight(self, board: Board, old_cell, new_cell):
        x1, y1 = board.get_indexes_by_cell(old_cell)
        x2, y2 = board.get_indexes_by_cell(new_cell)

        is_not_empty = board.get_fig_info(board.board[x2][y2])[1] != 'Empty'

        fig_info = board.get_fig_info(board.board[x1][y1])
        color = fig_info[0]
        type = fig_info[1]

        fig_info2 = board.get_fig_info(board.board[x2][y2])
        color2 = fig_info2[0]
        type2 = fig_info2[1]

        diff_colors = color != color2

        if ((abs(x2-x1)==2 and abs(y2-y1)==1) or (abs(x2-x1)==1 and abs(y2-y1)==2)) and (is_not_empty and diff_colors):
            return True

        return False

    def check_moves_knight(self, board: Board, old_cell, new_cell):
        res1 = self.check_knight_direct_move(board, old_cell, new_cell)
        res2 = self.check_capture_knight(board, old_cell, new_cell)

        return res1 or res2


class Bishop(Figure):
    def __init__(self, color, cell):
        super().__init__(color, cell)

    def check_bishop_direct_move(self, board: Board, old_cell, new_cell):
        x1, y1 = board.get_indexes_by_cell(old_cell)
        x2, y2 = board.get_indexes_by_cell(new_cell)

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
                    res2 = res2 and (board.get_fig_info(board.board[x][y])[1] == 'Empty')

            elif x2<x1 and y2>y1:
                res2 = True

                for i in range(1, N + 1):
                    x = x - i
                    y = y + i
                    res2 = res2 and (board.get_fig_info(board.board[x][y])[1] == 'Empty')

            elif x2>x1 and y2<y1:
                res2 = True

                for i in range(1, N + 1):
                    x = x + i
                    y = y - i
                    res2 = res2 and (board.get_fig_info(board.board[x][y])[1] == 'Empty')

            elif x2>x1 and y2>y1:
                res2 = True

                for i in range(1, N + 1):
                    x = x + i
                    y = y + i
                    res2 = res2 and (board.get_fig_info(board.board[x][y])[1] == 'Empty')

        return res1 and res2

    def check_capture_bishop(self, board: Board, old_cell, new_cell):
        """
        проверяет может ли ладья брать фигуру

        :param board:
        :param old_cell:
        :param new_cell:
        :return:
        """
        x1, y1 = board.get_indexes_by_cell(old_cell)
        x2, y2 = board.get_indexes_by_cell(new_cell)

        fig_info = board.get_fig_info(board.board[x1][y1])
        color = fig_info[0]
        type  = fig_info[1]

        fig_info2 = board.get_fig_info(board.board[x2][y2])
        color2 = fig_info2[0]
        type2 = fig_info2[1]

        is_not_empty = board.get_fig_info(board.board[x2][y2])[1] != 'Empty'
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
            res = self.chekc_bishop_direct_move(board, old_cell, new)
        else:
            res = True

        return is_not_empty and is_diff_colors and res

    def check_moves_bishop(self, board: Board, old_cell, new_cell):
        res1 = self.chekc_bishop_direct_move(board, old_cell, new_cell)
        res2 = self.check_capture_bishop(board, old_cell, new_cell)

        return res1 or res2


class Queen(Figure):
    def __init__(self, color, cell):
        super().__init__(color, cell)

    def check_queen_direct_move(self, board: Board, old_cell, new_cell):
        r = Rook(self.color, self.cell)
        b = Bishop(self.color, self.cell)
        res1 = r.check_rook_direct_move(board, old_cell, new_cell)
        res2 = b.check_bishop_direct_move(board, old_cell, new_cell)

        return res1 or res2

    def check_capture_queen(self, board: Board, old_cell, new_cell):
        r = Rook(self.color, self.cell)
        b = Bishop(self.color, self.cell)
        res1 = r.check_capture_rook(board, old_cell, new_cell)
        res2 = b.check_capture_bishop(board, old_cell, new_cell)

        return res1 or res2

    def CheckMovesQueen(self, board: Board, old_cell, new_cell):
        res1 = self.check_queen_direct_move(board, old_cell, new_cell)
        res2 = self.check_capture_queen(board, old_cell, new_cell)
        return res1 or res2


class King(Figure):
    def __init__(self, color, cell):
        super().__init__(color, cell)

    def check_king_direct_move(self, board: Board, old_cell, new_cell):
        x1, y1 = board.get_indexes_by_cell(old_cell)
        x2, y2 = board.get_indexes_by_cell(new_cell)

        fig_info = board.get_fig_info(board.board[x1][y1])
        color = fig_info[0]
        type = fig_info[1]

        fig_info2 = board.get_fig_info(board.board[x2][y2])
        color2 = fig_info2[0]
        type2 = fig_info2[1]

        is_empty = board.get_fig_info(board.board[x2][y2])[1] == 'Empty'
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

        i,j = board.search_fig(board, 'king', opposite_color)
        enemy_king_cell = board.get_cell_by_indexes(i, j)
        x,y = board.get_indexes_by_cell(enemy_king_cell)

        if ((abs(y2-y)==1) and (abs(x2-x)<=1)) or ((abs(x2-x)==1) and (abs(y2-y)<=1)):
            res2 = False
        else:
            res2 = True

        return res & res2

    def check_capture_king(self, board: Board, old_cell, new_cell):
        x1, y1 = board.get_indexes_by_cell(old_cell)
        x2, y2 = board.get_indexes_by_cell(new_cell)

        fig_info = board.get_fig_info(board.board[x1][y1])
        color = fig_info[0]
        type = fig_info[1]

        fig_info2 = board.get_fig_info(board.board[x2][y2])
        color2 = fig_info2[0]
        type2 = fig_info2[1]

        is_not_empty = board.get_fig_info(board.board[x2][y2])[1] != 'Empty'
        is_diff_colors = color != color2
        is_not_enemy_king = type2 != 'king'

        res = False
        if (abs(x2 - x1) == 1 or abs(y2 - y1) == 1) and is_not_empty and is_diff_colors and is_not_enemy_king:
            return True
        else:
            return False

    def chekc_moves_king(self, board: Board, old_cell, new_cell):
        res1 = self.check_king_direct_move(board, old_cell, new_cell)
        res2 = self.check_capture_king(board, old_cell, new_cell)
        return res1 or res2


    


if __name__ == '__main__':
    board = Board() # создаем объект класса
    board.output_board() # печатаем доску
    board.arrange_figures() # расставляем фигуры
    board.output_board() # печатаем доску