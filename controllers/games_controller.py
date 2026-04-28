from fastapi import APIRouter, HTTPException
from domain.models.view_models.game_vm import GameCreate, GameUpdate, GameResponse
from domain.interfaces.service_interfaces import IGameService
from typing import List

class GamesController:
    def __init__(self, games_service: IGameService):
        self.router = APIRouter(prefix="/games", tags=["games"])
        self.games_service = games_service
        self.setup_routes()

    def setup_routes(self):
        self.router.add_api_route("", self.get_games, methods=["GET"], response_model=List[GameResponse])
        self.router.add_api_route("/genres", self.get_genres, methods=["GET"])
        self.router.add_api_route("/{game_id}", self.get_game_by_id, methods=["GET"], response_model=GameResponse)
        self.router.add_api_route("", self.create_game, methods=["POST"], response_model=GameResponse)
        self.router.add_api_route("/{game_id}", self.update_game, methods=["PUT"])
        self.router.add_api_route("/{game_id}", self.delete_game, methods=["DELETE"])

    def get_games(self):
        return self.games_service.get_games()

    def get_genres(self):
        return self.games_service.get_genres()

    def get_game_by_id(self, game_id: int):
        game = self.games_service.get_game_by_id(game_id)
        if game is None:
            raise HTTPException(status_code=404, detail="Гру не знайдено")
        return game

    def create_game(self, game: GameCreate):
        return self.games_service.create_game(game)

    def update_game(self, game_id: int, game: GameUpdate):
        return self.games_service.update_game(game_id, game)

    def delete_game(self, game_id: int):
        return self.games_service.delete_game(game_id)
