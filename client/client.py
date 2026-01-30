import socket
import time

HOST = '127.0.0.1'
PORT = 65432
BUFFER_SIZE = 4096

COMMANDS = [
    'HELLO',
    'TIME',
    'ECHO Automated client test',
    'GET example.txt',
    'QUIT'
]


def recv_line(sock):
    buffer = ""
    while "\n" not in buffer:
        data = sock.recv(BUFFER_SIZE)
        if not data:
            break
        buffer += data.decode(errors="ignore")
    return buffer.strip()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))

        for cmd in COMMANDS:
            # Send command with newline (protocol requirement)
            client.sendall((cmd + "\n").encode())

            response = recv_line(client)
            print(f"> {cmd}\n{response}\n")

            time.sleep(1)


if __name__ == '__main__':
    main()
