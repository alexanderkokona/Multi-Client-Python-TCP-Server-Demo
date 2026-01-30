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
* Logs connections, requests, and errors to a rotating log file
* Applies basic hardening (timeouts, input length limits, graceful disconnects)

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
import logging
from datetime import datetime

HOST = '127.0.0.1'
PORT = 65432
FILES_DIR = 'files'
LOG_FILE = 'server.log'
MAX_REQUEST_SIZE = 1024
SOCKET_TIMEOUT = 60

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)


def handle_client(conn, addr):
    logging.info(f"Client connected: {addr}")
    conn.settimeout(SOCKET_TIMEOUT)

    try:
        with conn:
            while True:
                data = conn.recv(MAX_REQUEST_SIZE)
                if not data:
                    break

                request = data.decode(errors='ignore').strip()
                logging.info(f"Request from {addr}: {request}")

                response, close = process_request(request)
                conn.sendall(response.encode())

                if close:
                    break

    except socket.timeout:
        logging.warning(f"Connection timeout: {addr}")

    except Exception as e:
        logging.error(f"Error with {addr}: {e}")

    finally:
        logging.info(f"Client disconnected: {addr}")


def process_request(request):
    parts = request.split(maxsplit=1)
    command = parts[0].upper() if parts else ''

    if command == 'HELLO':
        return 'Hello, client!
', False

    elif command == 'TIME':
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '
', False

    elif command == 'ECHO':
        if len(parts) == 2:
            return parts[1] + '
', False
        return 'Usage: ECHO <message>
', False

    elif command == 'GET':
        if len(parts) != 2:
            return 'Usage: GET <filename>
', False

        filename = os.path.basename(parts[1])
        filepath = os.path.join(FILES_DIR, filename)

        if not os.path.isfile(filepath):
            return 'File not found.
', False

        with open(filepath, 'r') as file:
            return file.read() + '
', False

    elif command == 'QUIT':
        return 'Goodbye!
', True

    else:
        return 'Unknown command.
', False


def main():
    os.makedirs(FILES_DIR, exist_ok=True)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        logging.info(f"Server started on {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()


if __name__ == '__main__':
    main()
```

---python
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

```
        request = data.decode().strip()
        response = process_request(request)
        conn.sendall(response.encode())

print(f"[-] Disconnected: {addr}")
```

def process_request(request):
parts = request.split(maxsplit=1)
command = parts[0].upper()

```
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
```

def main():
os.makedirs(FILES_DIR, exist_ok=True)

```
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.bind((HOST, PORT))
    server.listen()
    print(f"[*] Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
```

if **name** == '**main**':
main()

````

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
            if not message:
                continue

            client.sendall(message.encode())

            response = client.recv(4096)
            print(response.decode())

            if message.upper() == 'QUIT':
                break


if __name__ == '__main__':
    main()
````

---

## client/auto_client.py

```python
import socket
import time

HOST = '127.0.0.1'
PORT = 65432

COMMANDS = [
    'HELLO',
    'TIME',
    'ECHO Automated client test',
    'GET example.txt',
    'QUIT'
]


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))

        for cmd in COMMANDS:
            client.sendall(cmd.encode())
            response = client.recv(4096)
            print(f"> {cmd}
{response.decode()}")
            time.sleep(1)


if __name__ == '__main__':
    main()
```

---python
import socket

HOST = '127.0.0.1'
PORT = 65432

def main():
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
client.connect((HOST, PORT))
print('Connected to server. Type commands or QUIT to exit.')

```
    while True:
        message = input('> ')
        client.sendall(message.encode())

        if message.upper() == 'QUIT':
            break

        response = client.recv(4096)
        print(response.decode())
```

if **name** == '**main**':
main()

```

---

## Demonstration Expectations

A successful demonstration shows:

- Server startup and log file creation
- Multiple manual clients connected simultaneously
- Automated client executing scripted commands
- Independent request handling without blocking
- Correct responses to each command
- Server-side logging of connections and requests
- Graceful client disconnects

---

## Demonstration Video Script

**1. Introduction (10–15 seconds)**  
Briefly explain the purpose of the project and the concepts it demonstrates.

**2. Server Startup (10 seconds)**  
Start the server and show the console/log file initializing.

**3. Manual Client Demo (30–45 seconds)**  
Connect one client and issue `HELLO`, `TIME`, and `ECHO` commands.

**4. Concurrent Clients (30 seconds)**  
Start a second manual client and show both interacting simultaneously.

**5. Automated Client (20 seconds)**  
Run `auto_client.py` to demonstrate scripted, repeatable interaction.

**6. File Retrieval (10 seconds)**  
Show `GET example.txt` and confirm correct output.

**7. Logging Proof (10 seconds)**  
Open `server.log` and highlight connection and request entries.

**8. Clean Shutdown (10 seconds)**  
Clients disconnect cleanly; server continues running.

---

## Final Notes

This version includes logging, automation, and basic hardening while remaining intentionally simple. It reflects realistic client/server design principles and provides a strong foundation for security monitoring, protocol design, and future expansion.

```
