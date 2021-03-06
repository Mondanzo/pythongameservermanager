from typing import Optional
import libtmux as tmux
from uuid import uuid4, UUID
from server.Wrappers import BaseGameServer
from typing import Dict


class GameServerManager:
	def __init__(self) -> None:
		 self.tmux = tmux.Server()
		 self.servers = Dict[UUID, BaseGameServer]

	def create_game_server(self, gsw: BaseGameServer, name: str):
		server = gsw(self.tmux, name)
		server.server_uuid
		pass

	def load_game_server(self, server):
		pass

	def get_gameserver_by_uuid(self, uuid: UUID or str) -> Optional[BaseGameServer]:
		return self.servers.get(uuid, None)

	def get_gameservers_by_types(self, type: BaseGameServer) -> Optional[BaseGameServer]:
		for server in self.servers.values():
			if isinstance(server, type):
				return server
		return None

	def get_gameserver_by_name(self, name) -> Optional[BaseGameServer]:
		for server in self.servers.values():
			if server.server_name == name:
				return server
		return None
