import os
import websockets
import json
import asyncio
import server.server_settings as server_settings
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from websockets.legacy.client import WebSocketClientProtocol
    from websockets.legacy.server import WebSocketServerProtocol

URI = f"ws://{server_settings.HOST}:{server_settings.PORT}"

class Client:
    def __init__(self, uri: str = None):
        if uri is None:
            self.uri = URI
        else:
            self.uri = uri
        self._job_id = None

    async def submit_to_server(self, job_filename: str):
        async with websockets.connect(uri=self.uri) as client:
            # Send token
            token = input("Please, insert your token\n")
            await client.send(token)

            response = await client.recv()
            print(response)

            # send file
            with open(job_filename, "r") as job_file:
                qasm_code = job_file.read()
            await client.send(qasm_code)

            # receive job id
            self._job_id =  await client.recv()

            await self.check_status(client)

    async def check_status(self, websocket: 'WebSocketClientProtocol'):
        while True:
            await websocket.send("status")
            response = await websocket.recv()
            response_data = json.loads(response)
            status = response_data.get("status")
            print(f"Task {self._job_id} status: {status}")

            if status == "completed":
                await websocket.send("get_result")
                result = await websocket.recv()
                print(result)
                self._save_results(result)
                break

            await asyncio.sleep(5)

    def _save_results(self, data):
        json_data = json.dumps(data)
        # write token data into json file
        file_path = f"results/job_{self._job_id}.json"
        with open(file_path, "w") as f:
            f.write(json_data)



if __name__ == '__main__':
    client = Client()
    asyncio.run(client.submit_to_server(job_filename="quantum_circuit.qasm"))



