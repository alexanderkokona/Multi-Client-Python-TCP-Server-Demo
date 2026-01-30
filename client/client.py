import socket

HOST = '127.0.0.1'
PORT = 65432


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        print('Connected to server. Type commands or QUIT to exit.')

        while True:
            message = input('> ')
            if not message:
                continue

            # Send newline-delimited command
            client.sendall((message + "\n").encode())

            response = client.recv(4096)
            print(response.decode())

            if message.upper() == 'QUIT':
                break


if __name__ == '__main__':
    main()
