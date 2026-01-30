# Multi-Client Python TCP Server Demo

## Overview

This project is a demonstration of a **multi-client TCP server application written in Python**. It showcases core concepts covered during the Sprint, including:

* Python fundamentals
* TCP socket networking
* Multithreading for concurrent clients
* File I/O for dynamic server responses
* Basic server hardening and logging

The server supports multiple simultaneous client connections and responds to structured, text-based client requests in real time.

---

## Learning Objectives Demonstrated

By completing this project, the following competencies are demonstrated:

* Creating TCP servers and clients using Python sockets
* Handling multiple concurrent connections using threading
* Designing and implementing a simple request/response protocol
* Performing safe, read-only file access on the server
* Implementing basic operational logging and timeouts
* Structuring a complete, maintainable networked application

---

## Project Structure

```
project-root/
│
├── server/
│   └── server.py
│
├── client/
│   ├── client.py
│   └── auto_client.py
│
├── files/
│   └── example.txt
│
└── README.md
```

---

## Request Protocol

Clients communicate with the server using simple **newline-delimited text commands**. Each command is sent as a single line terminated by a newline character (`\n`).

| Command    | Description                                   |
| ---------- | --------------------------------------------- |
| HELLO      | Receive a greeting from the server            |
| TIME       | Retrieve the current server time              |
| ECHO <msg> | Echo a message back to the client             |
| GET <file> | Retrieve contents of a predefined server file |
| QUIT       | Disconnect from the server                    |

All commands are case-insensitive.

---

## Server Behavior

* Listens on a fixed TCP port
* Accepts multiple client connections concurrently
* Spawns a dedicated thread per client
* Uses a line-based protocol to safely process input
* Performs **read-only file access** from the `/files` directory
* Logs connections, requests, errors, and timeouts to `server.log`
* Applies basic hardening measures:

  * Socket timeouts
  * Input buffering and size limits
  * Safe filename handling
  * Graceful client disconnects

---

## Client Behavior

### Manual Client (`client.py`)

* Connects to the server via TCP
* Accepts user input from the terminal
* Sends newline-delimited commands
* Displays server responses in real time
* Allows clean disconnection with `QUIT`

### Automated Client (`auto_client.py`)

* Connects to the server automatically
* Sends a predefined sequence of commands
* Demonstrates repeatable, scripted interaction
* Useful for testing and demonstrations

---

## How to Run

### 1. Start the Server

From the project root directory:

```bash
python3 server/server.py
```

The server will start listening and create a `server.log` file.

---

### 2. Start One or More Clients

In separate terminals, run one or more of the following:

```bash
python3 client/client.py
```

```bash
python3 client/auto_client.py
```

Multiple clients may be run simultaneously to demonstrate concurrent handling.

---

## Example Server File

**files/example.txt**

```
This is an example file stored on the server.
Clients may retrieve its contents using the GET command.
```

---

## Demonstration Expectations

A successful demonstration shows:

* Server startup and log file creation
* Multiple manual clients connected simultaneously
* Automated client executing scripted commands
* Independent request handling without blocking
* Correct responses to each command
* Server-side logging of connections and requests
* Graceful client disconnects

---

## Security and Design Considerations

* The server only allows read-only access to files in a predefined directory
* Filenames are sanitized to prevent path traversal
* Client inactivity is limited via socket timeouts
* Logging provides basic visibility into server activity

---

## Final Notes

This project intentionally avoids unnecessary complexity while remaining realistic and technically sound. It reflects real-world client/server design patterns and provides a strong foundation for more advanced networking, security monitoring, or protocol-based applications.

---

# Demonstration Video Script

## 1. Introduction (10–15 seconds)

"This project is a multi-client TCP server written in Python. It demonstrates socket networking, multithreading, file I/O, and basic server hardening. I’ll show the server handling multiple clients simultaneously and responding to different types of requests."

## 2. Server Startup (10 seconds)

* Start `server.py`
* Briefly point out the listening address and the creation of `server.log`

## 3. Manual Client Demonstration (30–45 seconds)

* Start `client.py`
* Issue the following commands:

  * `HELLO`
  * `TIME`
  * `ECHO Hello from client one`
* Explain that responses are returned in real time

## 4. Concurrent Clients (30 seconds)

* Start a second manual client in another terminal
* Show both clients sending commands at the same time
* Emphasize independent handling via threading

## 5. Automated Client Demonstration (20 seconds)

* Run `auto_client.py`
* Explain that it sends a scripted sequence of commands automatically
* Highlight its usefulness for testing and repeatability

## 6. File Retrieval (10 seconds)

* Demonstrate `GET example.txt`
* Show the server returning file contents

## 7. Logging Verification (10 seconds)

* Open `server.log`
* Point out connection, request, and disconnect entries

## 8. Clean Disconnect (10 seconds)

* Use `QUIT` to close clients cleanly
* Note that the server continues running and accepting new connections

---

**End of demonstration.**
