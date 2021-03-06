from os import PathLike
from pathlib import Path
from typing import Optional
import libtmux
from uuid import uuid4

class BaseConfig:
	def __init__(self) -> None:
		 pass
	pass

class BaseGameServer:

	def save_config(self):
		pass

	def load_config(self):
		pass

	def __init__(self, __tmux: libtmux.Server, name: str, path: PathLike, **kwargs) -> None:
		self.__tmux = __tmux
		self.session = Optional[libtmux.Session]
		self.server_uuid = kwargs["uuid"] or uuid4()
		self.server_folder = Path(path)
		self.server_name = name
		self.running = False
		pass


	def __get_session(self):
		if not self.__tmux.has_session(self.server_uuid):
			self.session = self.__tmux.new_session(
				session_name=self.server_uuid,
				window_name=self.server_name)
			self.session.set_environment()
		else:
			self.running = True	
			self.session = self.__tmux.find_where({
				"name": self.server_uuid
			})
		return self.session
		

	def start_server(self):
		raise NotImplementedError("The start_server method isn't implemented by this Wrapper. That is not good!")
