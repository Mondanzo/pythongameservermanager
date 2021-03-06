from webmanagerapi import GameServerManager
from server.Wrappers import MinecraftGameServer

if __name__ == "__main__":
	gsm = GameServerManager()
	gsm.create_game_server(MinecraftGameServer, "Minecraft Test Server")
	print(gsm.get_gameservers_by_types(MinecraftGameServer).server_name, gsm.get_gameservers_by_types(MinecraftGameServer).server_uuid)
