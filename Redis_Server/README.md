# Redis-Like Server

## Features
This project implements a **Redis-like server** in Python with key functionalities, modular design, and networking capabilities.

### Core Features:
1. **Command Handlers**:
    - Commands are categorized into groups:
        - **Key-Value Commands**: `GET`, `SET`, `DELETE`, `EXISTS`, `INCR`, `DECR`.
        - **List Commands**: `LPUSH`, `RPUSH`.
        - **Utility Commands**: `PING`, `ECHO`, `SAVE`.
    - Supports error handling for invalid and unknown commands.
2. **RESP Protocol**:
    - Serialization (`RespSerializer`) and deserialization (`RespDeserializer`) of RESP (Redis Serialization Protocol).
3. **In-Memory Redis Database**:
    - Implements singleton pattern for the database.
    - Supports key expiry and snapshot persistence.
4. **TCP Socket Server**:
    - Handles multiple clients concurrently using **threading**.
5. **Tests**:
    - Comprehensive unit tests for all commands, handlers, and utilities.
6. **Clean Code Design**:
    - Uses Object-Oriented Programming features:
        - Abstract Base Classes, Factory Methods, Static Methods.


## Getting Started

### Prerequisites
- Python 3.8+
- **ncat** (Netcat replacement):
    - Download Ncat here: [https://nmap.org/ncat/](https://nmap.org/ncat/)
    - **What is Ncat?**  
      Ncat is a feature-packed networking utility that reads and writes data across networks from the command line. It supports TCP/UDP communication and can be used for testing network servers.

---

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Danitilahun/Coding-Challenges.git
   cd Redis_Server
   ```

2. Run the server:
   ```bash
   python server.py -H localhost -p 6378
   ```

   You should see:
   ```
   Server started. Listening on localhost:6378...
   ```

---

## How to Test the Server

### Using Ncat for Commands

Open **Command Prompt** and test various Redis commands.

1. **PING Command**:
   ```bash
   echo *1\r\n$4\r\nPING\r\n | ncat localhost 6378
   ```
   **Expected Output**:
   ```
   $4
   PONG
   ```

2. **ECHO Command**:
   ```bash
   echo *2\r\n$4\r\nECHO\r\n$11\r\nHello World\r\n | ncat localhost 6378
   ```
   **Expected Output**:
   ```
   $11
   Hello World
   ```

3. **SET Command**:
   ```bash
   echo *3\r\n$3\r\nSET\r\n$3\r\nkey\r\n$5\r\nvalue\r\n | ncat localhost 6378
   ```
   **Expected Output**:
   ```
   $2
   OK
   ```

4. **GET Command**:
   ```bash
   echo *2\r\n$3\r\nGET\r\n$3\r\nkey\r\n | ncat localhost 6378
   ```
   **Expected Output**:
   ```
   $5
   value
   ```
---

## Running Tests
To test the entire server and commands:

1. Run the test suite:
   ```bash
   python -m unittest discover -s tests
   ```

2. The tests include:
   - Command handlers (`GET`, `SET`, etc.).
   - RESP protocol serialization and deserialization.
   - End-to-end request handling.

---

## Key Takeaways
By building this Redis-like server, you will learn:
- **Network Programming**:
    - How to build TCP servers and clients using `socket`.
- **Threading**:
    - Concurrently handle multiple clients using threads.
- **RESP Protocol**:
    - Serialization and deserialization of Redis requests/responses.
- **Object-Oriented Programming**:
    - Abstract Base Classes, Factory Methods, and Static Methods.
- **Testing**:
    - Writing unit tests for handlers, protocols, and command logic.
- **Error Handling**:
    - Building custom exceptions for robust error reporting.

---

Happy Learning! 🎉