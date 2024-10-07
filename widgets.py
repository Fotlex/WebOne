import random

from PySide6 import QtCore
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QVBoxLayout, QLabel, QHBoxLayout


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
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        for i in range(10):
            row_layout = QHBoxLayout()
            for j in range(10):
                button = CoordinateButton(i, j)
                button.setIcon(QIcon('sprites/cloud.png'))
                button.setIconSize(QtCore.QSize(42, 42))
                button.setFixedSize(50, 50)
                button.clicked.connect(self.on_button_click)
                row_layout.addWidget(button)
            layout.addLayout(row_layout)

        self.setLayout(layout)

    def on_button_click(self):
        button = self.sender()
        if isinstance(button, CoordinateButton):
            print(f"Coordinates: ({button.x}, {button.y})")
            content = ['mine', 'cupcake', 'empty'][random.randint(0, 2)]
            button.setIcon(QIcon(f'sprites/{content}.png'))
            button.setIconSize(QtCore.QSize(42, 42))
            # button.setEnabled(False)
