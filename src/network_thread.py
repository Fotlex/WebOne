from PySide6.QtCore import QThread, Signal

from .network_manager import NetworkManager


class NetworkThread(QThread):
    network_initialized = Signal(bool)
    move_received = Signal(tuple)

    def __init__(self):
        super().__init__()
        self.network_manager = NetworkManager()

    def run(self):
        is_my_turn = self.network_manager.initialize_network()
        self.network_initialized.emit(is_my_turn)

    def listen_move(self):
        data = self.network_manager.receive_move()
        self.move_received.emit(data)

    def send_move(self, x, y, item):
        self.network_manager.send_move(x, y, item)
