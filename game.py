import sys

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import Qt, pyqtSignal

from denis import BLACK, WHITE, Pawn, King, Rook
from ch_board import Ui_MainWindow
from denis2 import Choise_color


class Chess(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.c = Choise_color()
        self.rc = ()

    def game(self):
        if self.current_player_color() == WHITE:
            self.statusBar().showMessage('Ход белых')
        else:
            self.statusBar().showMessage('Ход черных')
        row, col, row1, col1 = self.rc
        row, col = row // 60 - 1, col // 60 - 1
        row1, col1 = row1 // 60 - 1, col1 // 60 - 1
        coordinats = (row, col, row1, col1)
        if not self.correct_coords(row, col) or not self.correct_coords(row1, col1):
           return
        if self.is_castling(coordinats):
            if self.move_piece(row, col, row1, col1):
                self.clear_atfld()
                self.attack_field_func()
                dan = self.danger()
                if dan == "мат":
                    if self.current_player_color() == WHITE:
                        # показать окно о том, кто победил
                        # запускать окно с выбором цвета
                        return
                    return
            else:
                self.statusBar().showMessage('Координаты некорректны! Попробуйте другой ход!')
        else:
            if row == 0 and col == 4 and self.current_player_color() == WHITE and self.get_piece(0, 4) == King and \
                    self.get_piece(0, 4).poss_cast:

                if row1 == 0 and col1 == 2 and self.get_piece(0, 0) == Rook and \
                        self.get_piece(0, 0).poss_cast:
                    self.castling(0, 4, 0, 2, 0, 0, 0, 3)
                elif row1 == 0 and col1 == 6 and self.get_piece(0, 7) == Rook and \
                        self.get_piece(0, 7).poss_cast:
                    self.castling(0, 4, 0, 6, 0, 7, 0, 5)
            elif row == 7 and col == 4 and self.current_player_color() == BLACK and self.get_piece(7, 4) == King and \
                    self.get_piece(7, 4).poss_cast:
                if row1 == 7 and col1 == 2 and self.get_piece(0, 0) == Rook and \
                        self.get_piece(0, 0).poss_cast:
                    self.castling(7, 4, 7, 2, 7, 0, 7, 3)
                elif row1 == 7 and col1 == 6 and self.get_piece(0, 7) == Rook and \
                        self.get_piece(0, 7).poss_cast:
                    self.castling(7, 4, 7, 6, 7, 7, 7, 5)
        return

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.rc += (event.x, event.y)

    def exit(self):
        sys.exit(app.exec())

    def correct_coords(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def is_castling(self, coordinats):
        if coordinats == (0, 4, 0, 2) and \
                coordinats == (0, 4, 0, 6) and \
                coordinats == (7, 4, 7, 2) and \
                coordinats == (7, 4, 7, 6):
            return True
        return False

    def opponent(self, color):
        if color == WHITE:
            return BLACK
        return WHITE

    def current_player_color(self):
        return self.color

    #   def cell(self, row, col):
    #      if self.field[row][col] is None:
    #         return '  '
    #    piece = self.field[row][col].figure()
    #   color = piece.get_color()
    #  c = 'w' if color == WHITE else 'b'
    # return c + piece.char()

    def get_piece(self, row, col):
        return self.field[row][col].figure()

    def move_piece(self, row, col, row1, col1):
        # if not correct_coords(row, col) or not correct_coords(row1, col1):
        #    return False
        # if row == row1 and col == col1:
        #    return False
        if self.field[row][col].type is None:
            return False
        piece = self.field[row][col].figure()
        if piece.get_color() != self.color:
            return False
        dan = self.danger()
        if dan == "шах":
            self.ch = 1
        elif dan:
            return False
        else:
            self.ch = 0
        if self.field[row1][col1].type is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].figure().get_color() == self.opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return
        if piece == Pawn and ((self.color == WHITE and row1 == 7) or
                              (self.color == BLACK and row1 == 0)):
            piece = piece.metamorphose()
        self.field[row][col].type = None
        self.field[row1][col1].type = piece
        self.color = self.opponent(self.color)
        return True

    def castling(self, kr, kc, kr1, kc1, rr, rc, rr1, rc1):
        self.field[kr][kc].type = None
        self.field[kr1][kc1].type = King
        self.field[rr][rc].type = None
        self.field[rr1][rc1].type = Rook

    def attack_field_func(self):
        for r in range(8):
            for c in range(8):
                if self.field[r][c] and self.field[r][c].figure().get_color() != self.color:
                    self.attack_field = self.field[r][c].figure().paint_field(self, self.attack_field, r, c)

    def clear_atfld(self):
        self.attack_field = [[()] * 8 for _ in range(8)]

    def danger(self):
        for i in self.field:
            for j in i:
                if not j:
                    continue
                j = j.figure()
                if j.get_type() == "King" and j.get_color() == self.color:
                    return j.danger(self, self.attack_field, self.ch)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Chess()
    game.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
