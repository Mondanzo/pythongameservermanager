import asyncio
import argparse, sys
from asyncio.events import AbstractServer
from asyncio.protocols import BaseProtocol
from asyncio import transports
from asyncio.streams import StreamReader, StreamWriter
from pathlib import Path
from typing import Mapping, Optional, TypedDict

parser = argparse.ArgumentParser(description="Wrapper for GameServers")
parser.add_argument("command",  type=Path, help="The command to execute")
parser.add_argument("--socket", dest='socket', type=Path, help='The path for the socket file.')

clients = []

class Arguments(TypedDict):
	command: Path
	socket: Optional[Path]

class WrapperProtocol(asyncio.Protocol):
	def __init__(self, server: AbstractServer) -> None:
		self.transport = None
		self.server = server
		self.connected = False
	
	def connection_made(self, transport: transports.Transport) -> None:
		self.transport = transport
		self.connected = True
		clients.append(self)
		pass

	def connection_lost(self, exc: Optional[Exception]) -> None:
		self.connected = False
		clients.remove(self)
		pass

	def data_received(self, data: bytes) -> None:
		ddata = data.decode('utf-8')
		if ddata == "SIGTERM":
			for c in clients:
				c.transport.close()
			print("Goodbye.")
			self.server.close()
		elif ddata.startswith("broadcast: "):
			br_msg = ddata[11:]
			print("Broadcasting: " + br_msg)
			for c in clients:
				c.transport.write(br_msg.encode())
		else:
			print("Recieved: " + ddata)
			self.transport.write(ddata.encode())

async def main(args: Arguments):
	loop = asyncio.get_event_loop()
	socket = args.socket
	if not socket:
		socket = Path.cwd() / "wgsm-wrapper.sock"

	if socket.exists():
		socket.unlink()

	server = await loop.create_unix_server(
		lambda: WrapperProtocol(server),
		path=socket,
		start_serving=False
		)

	async with server:
		await server.start_serving()
		await server.wait_closed()


if __name__ == "__main__":
	args = parser.parse_args()
	asyncio.run(main(args))
