from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QMainWindow

from network_manager import NetworkManager
from widgets import *


class NetworkThread(QThread):
    networkInitialized = Signal(bool)

    def __init__(self):
        super().__init__()
        self.network_manager = NetworkManager()

    def run(self):
        is_my_turn = self.network_manager.initialize_network()
        self.networkInitialized.emit(is_my_turn)

    def send_cords(self, x: int, y: int, item: int):
        self.network_manager.send_move(x, y, item)


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setCentralWidget(StartWidget(self.open_game_window))

    def open_game_window(self):
        self.setCentralWidget(SearchWidget())
        self.network_thread = NetworkThread()
        self.setup_network()

    def setup_network(self):
        self.network_thread.networkInitialized.connect(self.on_network_initialized)
        self.network_thread.start()

    def on_network_initialized(self, is_my_turn):
        self.setCentralWidget(GameWidget(self.network_thread.network_manager))

    def closeEvent(self, event):
        self.network_thread.terminate()
        self.network_thread.wait()
        event.accept()
