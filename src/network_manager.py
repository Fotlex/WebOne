import json
import random
import socket
import threading
from typing import Tuple

from . import config
from .game_logic import GameLogic


class NetworkManager:
    def __init__(self):
        self.is_server = False
        self.client_socket = None
        self.server_ready = threading.Event()
        self.client_connected = threading.Event()

    def discover_peer_and_establish_role(self) -> str:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            s.bind(('', config.UDP_PORT))
            s.sendto(config.CLIENT_PASSWORD, ('<broadcast>', config.UDP_PORT))
            host = socket.gethostbyname(socket.gethostname())
            while True:
                data, addr = s.recvfrom(1024)
                if addr[0] == host:
                    continue

                if data == config.SERVER_PASSWORD:
                    return addr[0]

                if data == config.CLIENT_PASSWORD:
                    s.sendto(config.CLIENT_PASSWORD, addr)
                    if host > addr[0]:
                        continue
                    threading.Thread(target=self.start_server, args=(addr[0],), daemon=True).start()
                    self.server_ready.wait()
                    s.sendto(config.SERVER_PASSWORD, addr)
                    self.is_server = True
                    return addr[0]

    def start_server(self, client_ip) -> None:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('', config.TCP_PORT))
        server_socket.listen(1)
        print(f"Server listening on {socket.gethostbyname(socket.gethostname())}:{config.TCP_PORT}")
        self.server_ready.set()

        while True:
            client_socket, addr = server_socket.accept()
            if addr[0] == client_ip:
                break
            client_socket.close()
        print(f"Accepted connection from {addr}")
        self.client_socket = client_socket
        server_socket.close()
        self.client_connected.set()

    def connect_to_server(self, server_ip) -> None:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, config.TCP_PORT))
        self.client_socket = client_socket

    def initialize_network(self) -> Tuple:
        peer_ip = self.discover_peer_and_establish_role()
        print(peer_ip)

        if self.is_server:
            print("I'm server")
            self.client_connected.wait()
            field = GameLogic.generate_field()
            first_player = random.choice((True, False))
            data = json.dumps((field, not first_player))
            self.send_data(data.encode())
        else:
            print("I'm client")
            self.connect_to_server(peer_ip)
            print(f'Connected to server at {peer_ip}')
            field, first_player = json.loads(self.receive_data().decode())

        return field, first_player

    def send_data(self, data: bytes) -> None:
        try:
            self.client_socket.sendall(data)
        except Exception as e:
            print(f'Error sending data: {e}')

    def receive_data(self) -> bytes:
        try:
            return self.client_socket.recv(1024)
        except Exception as e:
            print(f'Error receiving data: {e}')
            return b""

    def send_move(self, row: int, col: int) -> None:
        move = f'{row},{col}'
        print(move)
        self.send_data(move.encode())

    def receive_move(self) -> Tuple[int, int]:
        data = self.receive_data().decode()
        row, col = (int(el) for el in data.split(','))
        return row, col
