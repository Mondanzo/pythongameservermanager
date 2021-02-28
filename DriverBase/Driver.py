import asyncio, sys
from asyncio import protocols
from pathlib import Path


class DriverProtocol(protocols.Protocol):
	def __init__(self, on_con_lost):
		self.on_con_lost = on_con_lost
		self.transport = None
		self.running = False
		self.input_queue = asyncio.Queue()

	def connection_made(self, transport):
		self.transport = transport
		self.running = True
		asyncio.create_task(self.messenger_loop())

	def data_received(self, data):
		print("Received:", data.decode())

	def error_received(self, exc):
		print('Error received:', exc)

	def connection_lost(self, exc):
		print("Connection closed")
		self.running = False
		self.on_con_lost.set_result(True)

	def send_message(self, msg):
		self.transport.write(msg.encode())

	async def messenger_loop(self):
		while self.running:
			if self.input_queue.empty():
				print("message:")
			char = sys.stdin.readline(1)
			if char == "\n" and not self.input_queue.empty():
				message = ""
				for _ in range(self.input_queue.qsize()):
					message += self.input_queue.get_nowait()
				self.send_message(message)
			elif char:
				await self.input_queue.put(char)
			await asyncio.sleep(0)



class BaseDriver:
	def __init__(self):
		self.loop = asyncio.get_event_loop()
		self.socket_path = Path.cwd() / "wgsm-wrapper.sock"
		if not self.socket_path.exists():
			return

		self.loop.run_until_complete(self.start())

	async def start(self):

		on_con_lost = self.loop.create_future()

		transport, protocol = await self.loop.create_unix_connection(lambda: DriverProtocol(on_con_lost), self.socket_path)

		try:
			await on_con_lost
		finally:
			transport.close()
		

if __name__ == "__main__":
	BaseDriver()
