from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QPushButton

from network_manager import NetworkManager


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
                button = QPushButton(f"{i},{j}")
                button.setFixedSize(50, 50)
                row_layout.addWidget(button)
            layout.addLayout(row_layout)

        self.setLayout(layout)


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.current_widget = SearchWidget()
        self.setCentralWidget(self.current_widget)
        network_manager = NetworkManager()
        is_my_turn = network_manager.initialize_network()
        self.setCentralWidget(GameWidget())

    def spawn_game_zone(self) -> None:
        pass
