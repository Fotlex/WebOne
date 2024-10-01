import socket
from typing import Any

import config


def find_server() -> Any:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.bind(('', 0))
        s.sendto(config.SERVER_PASSWORD, ('<broadcast>', config.UDP_PORT))
        s.settimeout(5)
        try:
            while True:
                data, addr = s.recvfrom(1024)
                if data == config.CLIENT_PASSWORD:
                    return addr[0]
        except socket.timeout:
            return None


def connect_server(ip: Any):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, config.TCP_PORT))
        while True:
            message = input()
            s.sendall(message.encode())
            data = s.recv(1024)
            print(data.decode())


if __name__ == '__main__':
    server_ip = find_server()
    print(server_ip)
    connect_server(server_ip)
