# Redis-like Server Documentation

## Project Overview
This project implements a Redis-like server that uses the **Redis Serialization Protocol (RESP)** to handle client-server communication. It supports key-value storage commands, list commands, and utility commands.

### Features
1. **Command-Based Implementation**:
   - **Key-Value Commands**: GET, SET, DELETE, EXISTS, INCR, DECR, etc.
   - **List Commands**: LPUSH, RPUSH.
   - **Utility Commands**: PING, ECHO, SAVE.
2. **Redis Database**:
   - In-memory key-value store with optional persistence using snapshots.
3. **Serialization and Deserialization**:
   - Custom RESP protocol handlers for serializing and deserializing client-server messages.
4. **Socket Server**:
   - A multithreaded TCP server that listens for incoming client connections and processes requests.
5. **Tests**:
   - Unit tests for all commands, deserialization, serialization, and server request handling.
6. **Threading**:
   - Concurrent handling of multiple clients.

---

## Learning Outcomes
Working on this project helps you understand:
- **Threading**: Using Python's `threading` module to handle multiple connections concurrently.
- **OOP in Python**:
   - Abstract base classes with `ABC` and `@abstractmethod`.
   - Static and class methods.
   - Singleton pattern for managing the database instance.
   - Factory methods.
- **Network Programming**:
   - Building TCP socket servers using Python's `socket` module.
   - Interacting with a server using command-line tools like **ncat**.
- **RESP Protocol**:
   - Designing custom serialization and deserialization logic for communication.
- **Unit Testing**:
   - Writing comprehensive unit tests for individual commands and server functionality.

---

## Setup Instructions
### Step 1: Clone the Repository
Clone the repository to your local machine:
```bash
git clone https://github.com/Danitilahun/Coding-Challenges.git
cd Redis_Server
```

### Step 2: Install Requirements
Ensure you have Python 3 installed and any dependencies.

### Step 3: Run the Redis-Like Server
Start the server using the following command:
```bash
python server.py -H localhost -p 6378
```
- Replace `localhost` and `6378` with your desired host and port if needed.

### Step 4: Download Ncat for Testing
[Ncat](https://nmap.org/ncat/) is a feature-packed networking utility for testing network-based servers.
- Download Ncat from the official Nmap site: [https://nmap.org/ncat/](https://nmap.org/ncat/).
- Ncat allows you to send RESP messages to the server for testing.

---

## Testing the Server

### 1. Verify Server is Running
Run the following command to check the `PING` command:
```bash
echo -e "*1\r\n$4\r\nPING\r\n" | ncat localhost 6378
```
Expected Response:
```bash
+PONG
```

### 2. Test ECHO Command
Send an ECHO command to the server:
```bash
echo -e "*2\r\n$4\r\nECHO\r\n$11\r\nHello World\r\n" | ncat localhost 6378
```
Expected Response:
```bash
$11\r\nHello World\r\n
```

### 3. Test SET and GET Commands
- **SET Command**:
   ```bash
   echo -e "*3\r\n$3\r\nSET\r\n$3\r\nkey\r\n$5\r\nvalue\r\n" | ncat localhost 6378
   ```
   Expected Response:
   ```bash
   +OK\r\n
   ```
- **GET Command**:
   ```bash
   echo -e "*2\r\n$3\r\nGET\r\n$3\r\nkey\r\n" | ncat localhost 6378
   ```
   Expected Response:
   ```bash
   $5\r\nvalue\r\n
   ```

### 4. Other Commands
- **INCR Command**:
   ```bash
   echo -e "*2\r\n$4\r\nINCR\r\n$7\r\ncounter\r\n" | ncat localhost 6378
   ```
   Expected Response:
   ```bash
   :1\r\n
   ```
- **EXISTS Command**:
   ```bash
   echo -e "*2\r\n$6\r\nEXISTS\r\n$3\r\nkey\r\n" | ncat localhost 6378
   ```
   Expected Response:
   ```bash
   :1\r\n
   ```

### 5. Test with Unknown Command
Send an unsupported command:
```bash
echo -e "*1\r\n$7\r\nUNKNOWN\r\n" | ncat localhost 6378
```
Expected Response:
```bash
-ERR Unsupported command `UNKNOWN`\r\n
```

---

## Running Unit Tests
To test all implemented functionality, run the following command:
```bash
python -m unittest discover -s tests
```
This will run all unit tests located in the `tests` directory.

---

## Supported Commands
Here is a list of supported commands:
1. **Utility Commands**:
   - PING: Test the connection.
   - ECHO: Echoes back input arguments.
   - SAVE: Saves data to a snapshot file.
2. **Key-Value Commands**:
   - SET: Set a key with a value.
   - GET: Get the value of a key.
   - DELETE: Delete one or more keys.
   - EXISTS: Check if keys exist.
   - INCR: Increment a key's integer value.
   - DECR: Decrement a key's integer value.
3. **List Commands**:
   - LPUSH: Push values to the left of a list.
   - RPUSH: Push values to the right of a list.

---

## Conclusion
This project provides a complete implementation of a Redis-like server that is lightweight, testable, and feature-packed. It is an excellent project for learning:
- Advanced Python concepts like threading, OOP, and error handling.
- Network programming with sockets.
- Communication protocols like RESP.

Happy Learning! 🎉
