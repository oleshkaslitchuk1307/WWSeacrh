from domain.interfaces.repository_interfaces import IFavoritesRepository
from domain.interfaces.service_interfaces import IActionsService, IConvertService

class ActionsService(IActionsService):
    def __init__(self, favorites_repository: IFavoritesRepository, convert_service: IConvertService):
        self.favorites_repository = favorites_repository
        self.convert_service = convert_service

    def add_favorite(self, user_id: int, game_id: int):
        return self.favorites_repository.add_favorite(user_id, game_id)

    def delete_favorite(self, user_id: int, game_id: int):
        return self.favorites_repository.delete_favorite(user_id, game_id)

    def get_favorite(self, user_id: int):
        rows = self.favorites_repository.get_favorites(user_id)
        return self.convert_service.games_to_list(rows)

