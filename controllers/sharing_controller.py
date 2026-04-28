from fastapi import APIRouter
from domain.interfaces.service_interfaces import ISharingService

class SharingController:
    def __init__(self, sharing_service: ISharingService):
        self.router = APIRouter(prefix="/sharing", tags=["sharing"])
        self.sharing_service = sharing_service
        self.setup_routes()

    def setup_routes(self):
        self.router.add_api_route("/{game_id}", self.share_game, methods=["POST"])
        self.router.add_api_route("/{game_id}", self.get_share, methods=["GET"])

    def share_game(self, game_id: int):
        link = self.sharing_service.share_game(game_id)
        return {'message': 'Посилання створено', "link": link}

    def get_share(self, game_id: int):
        link = self.sharing_service.share_game(game_id)
        return {'link': link}