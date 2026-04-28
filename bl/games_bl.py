from domain.interfaces.repository_interfaces import IGamesRepository
from domain.interfaces.service_interfaces import IGameService, IValidationService, IConvertService

class GameService(IGameService):
    def __init__(self, games_repository: IGamesRepository, validation_service: IValidationService, convert_service: IConvertService):
        self.games_repository = games_repository
        self.validation_service = validation_service
        self.convert_service = convert_service

    def get_games(self):
        rows = self.games_repository.get_all_games()
        return self.convert_service.games_to_list(rows)

    def get_game_by_id(self, game_id: int):
        row = self.games_repository.get_game_by_id(game_id)
        return self.convert_service.game_to_dict(row)

    def create_game(self, game):
        game_dict = game.model_dump()
        self.validation_service.validate_game(game_dict)
        return self.games_repository.create_game(game_dict)

    def update_game(self, game_id: int, game):
        game_dict = game.model_dump(exclude_unset=True)
        if "rating" in game_dict and game_dict["rating"] is not None and (game_dict["rating"] < 0 or game_dict["rating"] > 10):
            raise ValueError("Рейтинг гри має бути від 0 до 10")
        return self.games_repository.update_game(game_id, game_dict)

    def delete_game(self, game_id: int):
        return self.games_repository.delete_game(game_id)

    def get_genres(self):
        return self.games_repository.get_distinct_genres()