import sys

from .io import Interface
from .app import IPyCtrlApp
import asyncio

async def connect_stdin_stdout():
    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)
    w_transport, w_protocol = await loop.connect_write_pipe(asyncio.streams.FlowControlMixin, sys.stdout)
    writer = asyncio.StreamWriter(w_transport, w_protocol, reader, loop)
    return reader, writer

async def main():
    reader, writer = await connect_stdin_stdout();
    shellapp = IPyCtrlApp()
    shellapp.initialize()
    io_if = Interface(shellapp, reader, writer)
    return await io_if.start()
    
if __name__ == '__main__':
    asyncio.run(main())
    

# if __name__ == '__main__':
#     shellapp = IPyCtrlApp()
#     shellapp.initialize()
#     while True:
#         line = sys.stdin.readline()
#         try:
#             result = shellapp.shell.run_cell(line, silent=True)
#         except Exception as err:
#             pass
        


