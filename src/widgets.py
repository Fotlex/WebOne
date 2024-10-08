from PySide6 import QtCore
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QMessageBox

from .game_logic import GameLogic


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

        self.label = QLabel("Поиск игры...")
        layout.addWidget(self.label)


class GameWidget(QWidget):
    def __init__(self, network_thread, is_my_turn):
        super().__init__()
        print(is_my_turn)
        self.network_thread = network_thread
        self.game_logic = GameLogic(self.network_thread, is_my_turn)
        self.network_thread.move_received.connect(self.game_logic.receive_opponent_move)

        self.game_board = QWidget()
        board_layout = QVBoxLayout()

        self.score_label = QLabel()
        self.score_label.setStyleSheet("font-size: 24px; color: black;")
        self.update_score()

        self.buttons = []
        self.create_game_grid(board_layout)
        self.game_board.setLayout(board_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.score_label, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.game_board)
        self.setLayout(main_layout)

        self.game_logic.signal_emitter.move_received.connect(self.update_button)
        self.game_logic.signal_emitter.game_ended.connect(self.show_game_end)

        if not self.game_logic.is_my_turn:
            self.setEnabled(self.game_logic.is_my_turn)
            QTimer.singleShot(0, self.game_logic.wait_for_opponent_move)

    def create_game_grid(self, layout):
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

    def on_button_click(self):
        button = self.sender()
        x, y = button.x, button.y
        self.game_logic.make_move(x, y)

    def update_button(self, data):
        x, y, content = data
        button = self.buttons[x][y]
        button.setIcon(QIcon(f'sprites/{content}.png'))
        button.setIconSize(QtCore.QSize(42, 42))
        button.clicked.disconnect(self.on_button_click)
        self.update_score()
        self.setEnabled(self.game_logic.is_my_turn)

    def show_game_end(self, result):
        self.setEnabled(False)
        QMessageBox.information(self, "Конец игры", f"Игра окончена. {result}")

    def update_score(self):
        text = f"Ваш счет: {self.game_logic.my_score} | Счет противника: {self.game_logic.opponent_score}"
        self.score_label.setText(text)
