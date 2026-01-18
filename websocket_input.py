from __future__ import annotations

import asyncio
import json
import queue
import threading
from typing import Optional

import websockets

from action import Action
from input import Input

_ACTION_MAP = {
    "move_left": Action.MOVE_LEFT,
    "move_right": Action.MOVE_RIGHT,
    "rotate_left": Action.ROTATE_LEFT,
    "rotate_right": Action.ROTATE_RIGHT,
    "drop": Action.DROP,
}


class WebSocketServer:
    def __init__(self, host: str = "127.0.0.1", port: int = 8765):
        self.host = host
        self.port = port
        self._actions: "queue.SimpleQueue[Action]" = queue.SimpleQueue()
        self._clients: set = set()
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._ready = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        self._ready.wait()

    async def _start_server(self):
        return await websockets.serve(self._handler, self.host, self.port)

    def _run(self) -> None:
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        server = self._loop.run_until_complete(self._start_server())
        self._ready.set()
        self._loop.run_forever()
        server.close()
        self._loop.run_until_complete(server.wait_closed())

    async def _handler(self, websocket) -> None:
        self._clients.add(websocket)
        try:
            async for message in websocket:
                action = self._parse_action(message)
                if action is not None:
                    self._actions.put(action)
        finally:
            self._clients.discard(websocket)

    def _parse_action(self, message) -> Optional[Action]:
        action_name = None
        if isinstance(message, str):
            try:
                payload = json.loads(message)
                if isinstance(payload, dict):
                    action_name = payload.get("action")
            except json.JSONDecodeError:
                action_name = message.strip()
        if not action_name:
            return None
        return _ACTION_MAP.get(str(action_name).strip().lower())

    def pop_action(self) -> Optional[Action]:
        try:
            return self._actions.get_nowait()
        except queue.Empty:
            return None

    async def _broadcast(self, data: str) -> None:
        if not self._clients:
            return
        to_remove = []
        for client in list(self._clients):
            try:
                await client.send(data)
            except Exception:
                to_remove.append(client)
        for client in to_remove:
            self._clients.discard(client)

    def send_state(self, payload: dict) -> None:
        if not self._loop or not self._ready.is_set():
            return
        data = json.dumps(payload)
        asyncio.run_coroutine_threadsafe(self._broadcast(data), self._loop)


_shared_server: Optional[WebSocketServer] = None


def get_shared_server(host: str = "127.0.0.1", port: int = 8765) -> WebSocketServer:
    global _shared_server
    if _shared_server is None:
        _shared_server = WebSocketServer(host=host, port=port)
    return _shared_server


class WebSocketInput(Input):
    """Input implementation backed by a websocket server."""

    def __init__(self, host: str = "127.0.0.1", port: int = 8765):
        self._server = get_shared_server(host=host, port=port)

    def get_action(self) -> Optional[Action]:
        return self._server.pop_action()
