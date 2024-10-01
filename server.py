import socket
import config


def udp_listener() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(('', config.UDP_PORT))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while True:
            data, addr = s.recvfrom(1024)
            if data == config.SERVER_PASSWORD:
                s.sendto(config.CLIENT_PASSWORD, addr)


if __name__ == "__main__":
    udp_listener()
