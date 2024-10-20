from PySide6.QtCore import QThread, Signal

from .network_manager import NetworkManager


class NetworkThread(QThread):
    network_initialized = Signal(tuple)
    move_received = Signal(tuple)

    def __init__(self):
        super().__init__()
        self.network_manager = NetworkManager()

    def run(self):
        data = self.network_manager.initialize_network()
        self.network_initialized.emit(data)

    def listen_move(self):
        try:
            data = self.network_manager.receive_move()
            self.move_received.emit(data)
        except ValueError:
            pass

    def send_move(self, x, y):
        self.network_manager.send_move(x, y)
