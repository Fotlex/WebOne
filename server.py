import socket


def start_server():
    host = "localhost"
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Server is running and waiting for connections on {host}:{port}")
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Client connected from address: {addr}")

        message = client_socket.recv(1024).decode()
        print(f"Received message from client: {message}")

        client_socket.send("Message received".encode())

        client_socket.close()


if __name__ == "__main__":
    start_server()
