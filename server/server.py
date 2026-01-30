import socket
import threading
import os
import logging
from datetime import datetime

HOST = '127.0.0.1'
PORT = 65432
FILES_DIR = 'files'
LOG_FILE = 'server.log'
BUFFER_SIZE = 1024
SOCKET_TIMEOUT = 60

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)


def handle_client(conn, addr):
    logging.info(f"Client connected: {addr}")
    conn.settimeout(SOCKET_TIMEOUT)

    buffer = ""

    try:
        with conn:
            while True:
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    break

                buffer += data.decode(errors="ignore")

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    request = line.strip()

                    if not request:
                        continue

                    logging.info(f"Request from {addr}: {request}")

                    response, close_conn = process_request(request)
                    conn.sendall(response.encode())

                    if close_conn:
                        return

    except socket.timeout:
        logging.warning(f"Connection timeout: {addr}")

    except Exception as e:
        logging.error(f"Error with {addr}: {e}")

    finally:
        logging.info(f"Client disconnected: {addr}")


def process_request(request):
    parts = request.split(maxsplit=1)
    command = parts[0].upper() if parts else ""

    if command == "HELLO":
        return "Hello, client!\n", False

    elif command == "TIME":
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n", False

    elif command == "ECHO":
        if len(parts) == 2:
            return parts[1] + "\n", False
        return "Usage: ECHO <message>\n", False

    elif command == "GET":
        if len(parts) != 2:
            return "Usage: GET <filename>\n", False

        filename = os.path.basename(parts[1])
        filepath = os.path.join(FILES_DIR, filename)

        if not os.path.isfile(filepath):
            return "File not found.\n", False

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read() + "\n", False
        except Exception:
            return "Error reading file.\n", False

    elif command == "QUIT":
        return "Goodbye!\n", True

    else:
        return "Unknown command.\n", False


def main():
    os.makedirs(FILES_DIR, exist_ok=True)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()

        logging.info(f"Server started on {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()
            thread = threading.Thread(
                target=handle_client,
                args=(conn, addr),
                daemon=True
            )
            thread.start()


if __name__ == "__main__":
    main()
