from PySide6 import QtGui
from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QApplication

from game import GameWindow


class StartWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        self.button = QPushButton("Играть")
        self.button.clicked.connect(self.open_game_window)
        self.button.setFixedSize(250, 125)
        self.grid_layout.addWidget(self.button, 0, 0, 1, 1)  # Позиционируем кнопку в центре

        self.setWindowTitle("Стартовое окно")
        self.setGeometry(200, 50, 800, 600)

    def open_game_window(self):
        game_window = GameWindow()
        game_window.show()
        self.close()
