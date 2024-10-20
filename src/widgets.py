from PySide6 import QtCore
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QIcon, QPixmap, QPainter, QFont, QColor
from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QVBoxLayout, QLabel, QHBoxLayout

from . import config
from .end_game_dialog import EndGameDialog
from .game_logic import GameLogic


class CoordinateButton(QPushButton):
    def __init__(self, x, y, game_logic, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.x = x
        self.y = y
        self.game_logic = game_logic
        self.is_flagged = False
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.right_click)

    def right_click(self):
        if not self.game_logic.is_my_turn or self.game_logic.field[self.x][self.y] == -1:
            return
        self.toggle_flag()

    def toggle_flag(self):
        self.is_flagged = not self.is_flagged
        icon_path = 'sprites/flag.png' if self.is_flagged else 'sprites/cloud.png'
        self.setIcon(QIcon(icon_path))


class StartWidget(QWidget):
    def __init__(self, func):
        super().__init__()
        self.game_window = None

        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        self.button = QPushButton("Играть")
        self.button.clicked.connect(func)
        self.button.setFixedSize(250, 125)

        font = QFont('Comic Sans MS', 20, QFont.Weight.Bold)
        self.button.setFont(font)
        self.grid_layout.addWidget(self.button, 0, 0, 1, 1)

        self.setWindowTitle("Стартовое окно")
        self.setGeometry(200, 50, 800, 600)


class SearchWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.label = QLabel("Поиск игры...")
        font = QFont('Comic Sans MS', 15, QFont.Weight.Bold)
        self.label.setFont(font)
        layout.addWidget(self.label)


class GameWidget(QWidget):
    def __init__(self, network_thread, field, is_my_turn):
        super().__init__()
        print("First turn:", is_my_turn)
        self.network_thread = network_thread
        self.game_logic = GameLogic(self.network_thread, field, is_my_turn)
        self.network_thread.move_received.connect(self.game_logic.receive_opponent_move)

        self.game_board = QWidget()
        board_layout = QVBoxLayout()

        self.score_label = QLabel()
        font = QFont('Comic Sans MS', 15, QFont.Weight.Bold)
        self.score_label.setFont(font)
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
        self.game_logic.delayTimer.timeout.connect(self.update_enabled_state)

        if not self.game_logic.is_my_turn:
            self.setEnabled(self.game_logic.is_my_turn)
            QTimer.singleShot(0, self.game_logic.wait_for_opponent_move)

    def create_game_grid(self, layout):
        for i in range(config.FIELD_SIZE):
            self.buttons.append([])
            row_layout = QHBoxLayout()
            for j in range(config.FIELD_SIZE):
                button = CoordinateButton(i, j, self.game_logic)
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
        self.game_logic.make_move(button, x, y)

    def update_enabled_state(self):
        self.setEnabled(self.game_logic.is_my_turn)

    def update_button(self, data):
        x, y, content = data
        button = self.buttons[x][y]
        if isinstance(content, str):
            button.setIcon(QIcon(f'sprites/{content}.png'))
        else:
            pixmap = self.generate_number_image(content)
            button.setIcon(QIcon(pixmap))
        button.setIconSize(QtCore.QSize(42, 42))
        button.clicked.disconnect(self.on_button_click)
        self.update_score()

    def show_game_end(self, data):
        self.setEnabled(False)
        game_status, winner_status = data
        dialog = EndGameDialog(self, self.game_logic, game_status, winner_status)
        dialog.exec_()

    def update_score(self):
        my_score_text = f"Ваш счет: {self.game_logic.my_score}"
        opponent_score_text = f"Счет противника: {self.game_logic.opponent_score}"
        mines_left_text = f"Осталось мин: {self.game_logic.mine_cells_left}"

        text = f"{my_score_text} | {opponent_score_text} | {mines_left_text}"
        self.score_label.setText(text)

    @staticmethod
    def generate_number_image(number):
        pixmap = QPixmap(50, 50)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        font = QFont('Comic Sans MS', 28, QFont.Weight.Bold)

        painter.setFont(font)
        painter.setPen(QColor("#80FF00"))

        rect = pixmap.rect().adjusted(2, 2, -2, -2)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(number))
        painter.end()
        return pixmap
