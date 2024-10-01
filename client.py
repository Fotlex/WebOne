import socket


def start_client(message):
    server_ip = "localhost"
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, port))

    client_socket.send(message.encode())

    response = client_socket.recv(1024).decode()
    print(f"Response from server: {response}")

    client_socket.close()


if __name__ == "__main__":
    text = input("Enter a message for the server: ")
    start_client(text)
