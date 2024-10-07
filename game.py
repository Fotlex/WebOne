from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QMainWindow

from network_manager import NetworkManager
from widgets import *


class NetworkThread(QThread):
    networkInitialized = Signal(bool)
    move_received = Signal(tuple)

    def __init__(self):
        super().__init__()
        self.network_manager = NetworkManager()

    def run(self):
        is_my_turn = self.network_manager.initialize_network()
        self.networkInitialized.emit(is_my_turn)

    def listen_move(self):
        data = self.network_manager.receive_move()
        self.move_received.emit(data)

    def send_move(self, x, y, item):
        self.network_manager.send_move(x, y, item)


class GameWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.network_thread = None
        self.setCentralWidget(StartWidget(self.open_game_window))

    def open_game_window(self):
        self.setCentralWidget(SearchWidget())
        self.network_thread = NetworkThread()
        self.setup_network()

    def setup_network(self):
        self.network_thread.networkInitialized.connect(self.on_network_initialized)
        self.network_thread.start()

    def on_network_initialized(self, is_my_turn):
        game_widget = GameWidget(self.network_thread, is_my_turn)
        self.setCentralWidget(game_widget)

    def closeEvent(self, event):
        if self.network_thread:
            self.network_thread.terminate()
            self.network_thread.wait()
        event.accept()
