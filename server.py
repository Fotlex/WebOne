import socket
import threading

import config


def udp_listener() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(('', config.UDP_PORT))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while True:
            data, addr = s.recvfrom(1024)
            if data == config.SERVER_PASSWORD:
                s.sendto(config.CLIENT_PASSWORD, addr)


def handle_client(conn, addr):
    print(f"Connected by {addr}")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(f"Received: {data.decode()}")
            msg = input('Text: ')
            conn.sendall(msg.encode())
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        conn.close()


def tcp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', config.TCP_PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()


if __name__ == "__main__":
    threading.Thread(target=udp_listener, daemon=True).start()
    tcp_server()
