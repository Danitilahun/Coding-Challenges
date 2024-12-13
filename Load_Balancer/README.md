# Load Balancer with Simple HTTP Servers

This project implements a **Load Balancer** with **Simple HTTP Servers**, demonstrating key principles of load balancing, threading, and distributed system design. The system uses a **Round Robin** algorithm to distribute requests, dynamically monitors server health, and ensures high availability.

---

## Features

- **Simple HTTP Server**: Simulates a backend server responding to HTTP requests with a predefined response.
- **Backend Server**: Manages bidirectional communication between clients and backend systems using threading.
- **Load Balancer**:
  - Distributes requests across backend servers using the **Round Robin** algorithm.
  - Dynamically monitors the health of backend servers and adjusts routing accordingly.
- **Health Checks**:
  - Periodically sends HTTP requests to backend servers' `/health` endpoints.
  - Dynamically updates server states (`is_up`) based on their availability and response status.
  - Ensures that unhealthy servers are excluded from request routing until they recover.
- **Multithreading**:
  - Used extensively throughout the project to handle concurrent operations, such as:
    - **Health Checks**: Each backend server is monitored in a separate thread.
    - **Client-Server Communication**: Bidirectional data flow between clients and backend servers is managed using two threads per connection.
    - **Load Balancer Operations**: Multiple threads handle concurrent client requests and backend interactions.

---

## How It Works

### **1. Simple HTTP Server**
- **Purpose**: Simulates backend servers that handle client requests and send back a predefined HTTP response.
- **Location**: `src/simple_http_server/simple_http_server.py`
- **Key Features**:
  - Listens for incoming TCP connections.
  - Responds to requests with a simple HTTP message.

### **2. Backend Server**
- **Purpose**: Acts as an intermediary between the client and the load balancer.
- **Location**: `src/backend/backend_server.py`
- **Key Features**:
  - Handles bidirectional communication with clients.
  - Uses threads to forward data between clients and backend services.
  - Maintains server state, including `is_up` for health monitoring.

### **3. Load Balancer**
- **Purpose**: Routes incoming client requests to backend servers using the **Round Robin** algorithm.
- **Location**: `src/load_balancer/load_balancer.py`
- **Key Features**:
  - Dynamically adjusts routing based on server health.
  - Uses threads to handle multiple client connections concurrently.

### **4. Health Checks**
- **Purpose**: Monitors backend server availability and updates their status dynamically.
- **Location**: `src/healthcheck/health_check.py`
- **Key Features**:
  - Sends periodic HTTP GET requests to backend servers' `/health` endpoints.
  - Marks servers as `is_up = False` if they fail health checks or are unreachable.
  - Automatically reintegrates recovered servers into the pool.

---

## Multithreading

### **Why Use Multithreading?**
Multithreading ensures that critical operations like health checks, client-server communication, and backend interactions run concurrently without blocking the system.

### **Threading Examples**
1. **Health Checks**:
   - Each server has a dedicated thread for health monitoring.
   - Example:
     ```python
     health_check_thread = Thread(target=health_checker.health_check)
     health_check_thread.start()
     ```

2. **Bidirectional Communication**:
   - Two threads are used per client connection:
     - **Client to Server**: Forwards client requests to the backend.
     - **Server to Client**: Sends backend responses back to the client.
   - Example:
     ```python
     client_to_backend = threading.Thread(target=forward_data, args=(client_connection, backend_connection))
     backend_to_client = threading.Thread(target=forward_data, args=(backend_connection, client_connection))
     ```

3. **Concurrent Request Handling**:
   - Multiple threads allow the load balancer to serve multiple clients simultaneously.

---

### **Summary of Thread Usage**

| **Threaded Operation**        | **Purpose**                                                                 |
|--------------------------------|-----------------------------------------------------------------------------|
| **Health Checks**              | Monitor server health without interrupting other load balancer operations.  |
| **Bidirectional Communication**| Handle simultaneous data flow between clients and backend servers.          |
| **Concurrent Request Handling**| Serve multiple clients concurrently, ensuring high availability and scalability. |

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Danitilahun/Coding-Challenges.git
cd Load_Balancer
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Running the Project

### 1. Start Simple HTTP Servers
Run the simple HTTP servers to simulate backend servers:

```bash
python server.py --host 127.0.0.1 --port 5001
python server.py --host 127.0.0.1 --port 5002
python server.py --host 127.0.0.1 --port 5003
```

### 2. Configure Server Database
Ensure `server_db.json` is updated with backend server details:
```json
{
  "server_list": [
    {"id": 1, "host": "127.0.0.1", "port": 5001},
    {"id": 2, "host": "127.0.0.1", "port": 5002},
    {"id": 3, "host": "127.0.0.1", "port": 5003}
  ]
}
```

### 3. Start the Load Balancer
Run the load balancer to distribute requests across backend servers:
```bash
python load_balancer.py --host 127.0.0.1 --port 5432 --health-check-interval 15
```

### 4. Send Requests to the Load Balancer
Use a tool like `curl` or Postman to send requests to the load balancer:
```bash
curl http://127.0.0.1:5432
```

---

## Example Workflow

1. Start three Simple HTTP Servers on ports `5001`, `5002`, and `5003`.
2. Configure `server_db.json` with their details.
3. Start the Load Balancer on `127.0.0.1:5432`.
4. Send client requests to the Load Balancer:
   - The Load Balancer distributes requests to backend servers using Round Robin.
   - Unhealthy servers are skipped automatically.

---
