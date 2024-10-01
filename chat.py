import socket
import threading
from typing import Any

import config


def find_server() -> Any:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.bind(('', config.UDP_PORT))
        s.sendto(config.SERVER_PASSWORD, ('<broadcast>', config.UDP_PORT))
        s.settimeout(10)
        host = socket.gethostbyname(socket.gethostname())
        try:
            while True:
                data, addr = s.recvfrom(1024)
                if data == config.SERVER_PASSWORD and addr[0] != host:
                    s.sendto(config.SERVER_PASSWORD, addr)
                    return addr[0]
        except socket.timeout:
            return None


def handle_client(client_socket, client_address):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(f"Received from {client_address}: {message}")
            else:
                break
        except Exception as e:
            print(f"Error handling client: {e}")
            break
    client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', config.TCP_PORT))
    server.listen(5)
    print(f"Server listening on {socket.gethostbyname(socket.gethostname())}:{config.TCP_PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()


def send_message(server_ip_address):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((server_ip_address, config.TCP_PORT))
        while True:
            message = input()
            if message.lower() == 'exit':
                break
            s.sendall(message.encode())


if __name__ == '__main__':
    server_ip = find_server()
    print(f"Server IP found: {server_ip}")

    server_thread = threading.Thread(target=start_server)
    server_thread.start()

    if server_ip:
        send_message(server_ip)
    else:
        print("No server found. This instance will act only as a server.")
        server_thread.join()
