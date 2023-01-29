from asyncio import FIRST_COMPLETED, Condition, Event, Semaphore, StreamWriter, StreamReader, Task, tasks
import asyncio
import json
from typing import Dict, List
from .app import IPyCtrlApp


class Interface:
    istream: StreamReader
    ostream: StreamWriter
    tasks: List[Task]

    app: IPyCtrlApp

    def __init__(
        self, app: IPyCtrlApp, in_stream: StreamReader, out_stream: StreamWriter
    ) -> None:
        self.app = app
        self.istream = in_stream
        self.ostream = out_stream
        self.cond = Event()
        self.tasks = []

        self.handlers = {
            "run_cell": self.exec_cell
        }

    def decode(self, msg: bytes):
        return json.loads(msg)

    def encode(self, value):
        return json.dumps(value).encode('utf8') + b'\n'

    async def exec_cell(self, code):
        result = await self.app.shell.run_cell_async(code)
        return {
            "success": result.success,
            "result": repr(result.result),
            "info": repr(result.info)
        }

    async def route_message(self, message):
        if isinstance(message, Dict) \
           and (mt := message.pop("m", None)) \
           and (hndl := self.handlers.get(mt)):
            return await hndl(**message)
        else:
            return {"error": "no handler"}

    async def handle_message(self, value):
        data = self.decode(value)
        handle_res = await self.route_message(data)
        res = self.encode(handle_res)
        self.ostream.write(res)
        await self.ostream.drain()

    async def _read_line(self):
        line = await self.istream.readline()
        # self.tasks.append(asyncio.create_task(self.handle_message(line)))
        self.create_task(self.handle_message(line))

    async def read_loop(self):
        await self._read_line()
        self.create_task(self.read_loop())
        return True

    def create_task(self, coro):
        self.tasks.append(asyncio.create_task(coro))
        self.cond.set()

    async def start(self):
        self.create_task(self.read_loop())
        while True:
            # while self.tasks == []:
            #     await self.cond.acquire()
            while len(self.tasks) == 0:
                await self.cond.wait()
                self.cond.clear()

            done, pending = await asyncio.wait(self.tasks, return_when=FIRST_COMPLETED)
            for d in done:
                await d
            self.tasks = list(pending)

