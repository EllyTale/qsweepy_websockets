# qsweepy_websockets
This project implements a simple WebSocket server that accepts tasks from clients, processes them sequentially, and sends the results back to the clients.
The server runs asynchronously to handle multiple clients efficiently. This project consists of two main components:

1. **server.py**: The WebSocket server that receives and processes tasks.
2. **client.py**: A simple client that connects to the server, sends tasks, and receives results.

## Prerequisites

Before running the server and client, make sure you have Python 3.12+ installed. Additionally, the following Python packages are required:

- `websockets`: To manage WebSocket connections.
- `asyncio`: To handle asynchronous tasks.
- `json`: To handle JSON data transfer.