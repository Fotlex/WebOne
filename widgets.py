import random

from PySide6 import QtCore
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QMessageBox


class CoordinateButton(QPushButton):
    def __init__(self, x, y, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.x = x
        self.y = y


class StartWidget(QWidget):
    def __init__(self, func):
        super().__init__()
        self.game_window = None

        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        self.button = QPushButton("Играть")
        self.button.clicked.connect(func)
        self.button.setFixedSize(250, 125)
        self.grid_layout.addWidget(self.button, 0, 0, 1, 1)

        self.setWindowTitle("Стартовое окно")
        self.setGeometry(200, 50, 800, 600)


class SearchWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("Поиск игры: ")
        layout.addWidget(self.label)


class GameWidget(QWidget):
    def __init__(self, network_manager, is_my_turn):
        super().__init__()
        print(is_my_turn)
        self.network_manager = network_manager
        self.is_my_turn = is_my_turn
        self.buttons_left = 100
        self.my_score = 0
        self.opponent_score = 0
        layout = QVBoxLayout()
        self.score_label = QLabel(f"Ваш счет: {self.my_score} | Счет противника: {self.opponent_score}")
        layout.addWidget(self.score_label)

        self.buttons = []
        for i in range(10):
            self.buttons.append([])
            row_layout = QHBoxLayout()
            for j in range(10):
                button = CoordinateButton(i, j)
                button.setIcon(QIcon('sprites/cloud.png'))
                button.setIconSize(QtCore.QSize(42, 42))
                button.setFixedSize(50, 50)
                button.clicked.connect(self.on_button_click)
                row_layout.addWidget(button)
                self.buttons[i].append(button)
            layout.addLayout(row_layout)

        self.setLayout(layout)
        if not self.is_my_turn:
            self._wait_for_opponent_move()

    def on_button_click(self):
        if not self.is_my_turn:
            return
        button = self.sender()

        print(f"Coordinates: ({button.x}, {button.y})")
        rnd = random.randint(0, 2)
        content = ['mine', 'empty', 'cupcake'][rnd]
        self.my_score += rnd - 1
        button.setIcon(QIcon(f'sprites/{content}.png'))
        button.setIconSize(QtCore.QSize(42, 42))
        button.clicked.disconnect(self.on_button_click)

        self.network_manager.send_move(button.x, button.y, rnd)
        self.is_my_turn = False
        self._update_score()
        self._wait_for_opponent_move()

    def _wait_for_opponent_move(self):
        self.setEnabled(False)
        QtCore.QTimer.singleShot(0, self._check_opponent_move)

    def _check_opponent_move(self):
        if self.buttons_left > 0:
            row, col, item = self.network_manager.receive_move()
            button = self.buttons[row][col]
            content = ['mine', 'empty', 'cupcake'][item]
            button.setIcon(QIcon(f'sprites/{content}.png'))
            self.opponent_score += item - 1
            button.clicked.disconnect(self.on_button_click)
            self._update_score()
            self.is_my_turn = True
            self.setEnabled(True)
        else:
            self._end_game()

    def _update_score(self):
        self.buttons_left -= 1
        self.score_label.setText(f"Ваш счет: {self.my_score} | Счет противника: {self.opponent_score}")
        if self.buttons_left == 0:
            self._end_game()

    def _end_game(self):
        winner = "Вы выиграли!" if self.my_score > self.opponent_score else "Вы проиграли!" if self.my_score < self.opponent_score else "Ничья!"
        QMessageBox.information(self, "Конец игры", f"Игра окончена. {winner}")
