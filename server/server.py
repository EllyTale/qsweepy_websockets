import websockets
import json
import asyncio
from collections import OrderedDict
from queue import Queue
import server_settings
from process import Process
import uuid
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from websockets.legacy.server import WebSocketServerProtocol


class Server:
    def __init__(self):
        self._job_queue = Queue()
        self._job_status = OrderedDict()
        self._job_results = {}

    async def ws_handler(self, websocket: 'WebSocketServerProtocol', path):
        try:
            # receive token
            token = await websocket.recv()
            client_name = self._check_token(token)
            await self._add_client(client_name, websocket)

            # receive file
            job = await websocket.recv()
            job_id = uuid.uuid4().hex
            self._job_status[job_id] = "in_queue"
            self._job_queue.put((job, job_id, websocket))

            # send job id
            await websocket.send(job_id)

            if self._job_queue.qsize() == 1:
                asyncio.create_task(self.process_job_queue())

            while True:
                status_request = await websocket.recv()
                if status_request == "status":
                    status = self._job_status.get(job_id, 'unknown')
                    response = json.dumps({"job_id": job_id, "status": status})
                    await websocket.send(response)

                elif status_request == "get_result" and self._job_status.get(job_id) == "completed":
                    response = json.dumps({"job_id": job_id, "results": self._job_results[job_id]})
                    await websocket.send(response)
                    break


        except websockets.exceptions.ConnectionClosed:
            print("Connection closed")
            self._remove_job_by_websocket(websocket)

    async def start_server(self):
        async with websockets.serve(self.ws_handler, server_settings.HOST, server_settings.PORT):
            print("Server is starting")
            try:
                await asyncio.Future()  # to run forever
            except asyncio.CancelledError:
                print("Server was stopped")

    @staticmethod
    def _check_token(token: str):
        with open(server_settings.TOKENS, "r") as f:
            clients_tokens = json.load(f)

        for client_name, client_token in clients_tokens.items():
            if client_token == token:
                return client_name
        else:
            return None

    async def _add_client(self, client_name: str, websocket: 'WebSocketServerProtocol'):
        if client_name is not None:
            await websocket.send(f"Hello, {client_name}")
        else:
            await websocket.send(json.dumps({"error": "Invalid token"}))
            await websocket.close(code=1008, reason="Invalid token")  # Disconnect

    async def process_job_queue(self):
        while not self._job_queue.empty():
            job, job_id, _ = self._job_queue.get()
            self._job_status[job_id] = "running"
            print(f"Task {job_id} started, status: running")

            await self.process_job(job_id, job)
            self._job_queue.task_done()

            if self._job_queue.qsize() > 0:
                await self.process_job_queue()

    async def process_job(self, job_id: str, job):
        process = Process(job)
        result = await asyncio.to_thread(process.run)

        self._job_status[job_id] = "completed"
        print(f"Task {job_id} completed.")
        self._job_results[job_id] = result

    def _remove_job_by_websocket(self, websocket: 'WebSocketServerProtocol'):
        """Removes the job associated with the given websocket from the queue"""
        temp_queue = Queue()
        while not self._job_queue.empty():
            job, job_id, ws = self._job_queue.get()
            if ws != websocket:
                temp_queue.put((job, job_id, ws))
            else:
                del self._job_status[job_id]
                self._job_queue = temp_queue


if __name__ == '__main__':
    server = Server()
    asyncio.run(server.start_server())









