from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton

from game import GameWindow


class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.game_window = None

        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        self.button = QPushButton("Играть")
        self.button.clicked.connect(self.open_game_window)
        self.button.setFixedSize(250, 125)
        self.grid_layout.addWidget(self.button, 0, 0, 1, 1)

        self.setWindowTitle("Стартовое окно")
        self.setGeometry(200, 50, 800, 600)

    def open_game_window(self):
        self.game_window = GameWindow()
        self.game_window.show()
        self.close()
        self.game_window.setup_network()
