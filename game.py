from PySide6.QtCore import QThread, Signal, QTimer
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


class NetworkThread(QThread):
    networkInitialized = Signal(bool)

    def __init__(self):
        super().__init__()
        self.network_manager = NetworkManager()

    def run(self):
        is_my_turn = self.network_manager.initialize_network()
        self.networkInitialized.emit(is_my_turn)


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setCentralWidget(SearchWidget())
        self.network_thread = NetworkThread()

    def setup_network(self):
        self.network_thread.networkInitialized.connect(self.on_network_initialized)
        self.network_thread.start()

    def on_network_initialized(self, is_my_turn):
        self.setCentralWidget(GameWidget())

    def closeEvent(self, event):
        self.network_thread.terminate()
        self.network_thread.wait()
        event.accept()


def open_game_window(self):
    self.game_window = GameWindow()
    self.game_window.show()
    QTimer.singleShot(0, self.game_window.setup_network)
    self.close()
