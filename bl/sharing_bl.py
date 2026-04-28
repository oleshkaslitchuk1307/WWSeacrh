from domain.interfaces.service_interfaces import ISharingService

class SharingService(ISharingService):
    def share_game(self, game_id: int):
        return f'https://gamesearchsite.com/watch?v={game_id}'
