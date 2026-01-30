# Multi-Client Python TCP Server Demo

## Overview

This project is a demonstration of a **multi-client TCP server application written in Python**. It is designed to showcase core concepts covered during the Sprint:

* Python fundamentals
* TCP socket networking
* Multithreading for concurrent clients
* File I/O for dynamic server responses

The server accepts multiple client connections simultaneously and responds to structured client requests in real time.

---

## Learning Objectives Demonstrated

By completing this project, the following competencies are demonstrated:

* Creating TCP servers and clients using Python sockets
* Handling multiple concurrent connections with threading
* Designing a simple text-based request/response protocol
* Performing safe, read-only file access on the server
* Structuring a small but complete networked application

---

## Project Structure

```
project-root/
│
├── server/
│   └── server.py
│
├── client/
│   └── client.py
│
├── files/
│   └── example.txt
│
└── README.md
```

---

## Request Protocol

Clients communicate with the server using simple text commands:

| Command        | Description                                   |
| -------------- | --------------------------------------------- |
| HELLO          | Receive a greeting from the server            |
| TIME           | Retrieve the current server time              |
| ECHO <message> | Echo a message back to the client             |
| GET <filename> | Retrieve contents of a predefined server file |
| QUIT           | Disconnect from the server                    |

All commands are case-insensitive.

---

## Server Behavior

* Listens on a fixed TCP port
* Accepts multiple clients concurrently using threads
* Handles each client independently
* Performs **read-only file access** from the `/files` directory
* Logs connections and disconnections to the console

---

## Client Behavior

* Connects to the server using TCP
* Sends commands entered by the user
* Displays server responses in real time
* Allows clean disconnection

---

## How to Run

### 1. Start the Server

From the project root:

```bash
python3 server/server.py
```

### 2. Start One or More Clients

In separate terminals:

```bash
python3 client/client.py
```

You can run multiple clients simultaneously to demonstrate concurrent handling.

---

## Example File (`files/example.txt`)

```
This is an example file stored on the server.
Clients may retrieve its contents using the GET command.
```

---

## server/server.py

```python
import socket
import threading
import os
from datetime import datetime

HOST = '127.0.0.1'
PORT = 65432
FILES_DIR = 'files'


def handle_client(conn, addr):
    print(f"[+] Connected: {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            request = data.decode().strip()
            response = process_request(request)
            conn.sendall(response.encode())

    print(f"[-] Disconnected: {addr}")


def process_request(request):
    parts = request.split(maxsplit=1)
    command = parts[0].upper()

    if command == 'HELLO':
        return 'Hello, client!\n'

    elif command == 'TIME':
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n'

    elif command == 'ECHO':
        if len(parts) == 2:
            return parts[1] + '\n'
        return 'Usage: ECHO <message>\n'

    elif command == 'GET':
        if len(parts) != 2:
            return 'Usage: GET <filename>\n'

        filename = os.path.basename(parts[1])
        filepath = os.path.join(FILES_DIR, filename)

        if not os.path.isfile(filepath):
            return 'File not found.\n'

        with open(filepath, 'r') as file:
            return file.read() + '\n'

    elif command == 'QUIT':
        return 'Goodbye!\n'

    else:
        return 'Unknown command.\n'


def main():
    os.makedirs(FILES_DIR, exist_ok=True)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print(f"[*] Server listening on {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()


if __name__ == '__main__':
    main()
```

---

## client/client.py

```python
import socket

HOST = '127.0.0.1'
PORT = 65432


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))
        print('Connected to server. Type commands or QUIT to exit.')

        while True:
            message = input('> ')
            client.sendall(message.encode())

            if message.upper() == 'QUIT':
                break

            response = client.recv(4096)
            print(response.decode())


if __name__ == '__main__':
    main()
```

---

## Demonstration Expectations

A successful demonstration shows:

* Multiple clients connected simultaneously
* Independent request handling
* Correct responses to each command
* Safe file retrieval
* Clean client disconnects

---

## Final Notes

This project intentionally avoids unnecessary complexity while remaining realistic and technically sound. It reflects real-world client/server patterns and provides a strong foundation for more advanced networking or security-focused applications.
