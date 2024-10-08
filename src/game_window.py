from PySide6.QtWidgets import QMainWindow

from .network_thread import NetworkThread
from .widgets import *


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('WebOne')
        self.setWindowIcon(QIcon('sprites/cloud.png'))
        self.network_thread = None
        self.setCentralWidget(StartWidget(self.open_game_window))

    def open_game_window(self):
        self.setCentralWidget(SearchWidget())
        self.network_thread = NetworkThread()
        self.setup_network()

    def setup_network(self):
        self.network_thread.network_initialized.connect(self.on_network_initialized)
        self.network_thread.start()

    def on_network_initialized(self, is_my_turn):
        game_widget = GameWidget(self.network_thread, is_my_turn)
        self.setCentralWidget(game_widget)

    def closeEvent(self, event):
        if self.network_thread:
            self.network_thread.terminate()
            self.network_thread.wait()
        event.accept()
