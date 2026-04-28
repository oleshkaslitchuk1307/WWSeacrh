from fastapi import APIRouter, Depends
from bl.jwt_bl import get_current_user
from domain.interfaces.service_interfaces import IActionsService

class ActionsController:
    def __init__(self, actions_service: IActionsService):
        self.router = APIRouter(prefix="/actions", tags=["actions"])
        self.actions_service = actions_service
        self.setup_routes()

    def setup_routes(self):
        self.router.add_api_route("/favorites", self.get_favorite, methods=["GET"])
        self.router.add_api_route("/favorites/{game_id}", self.add_favorite, methods=["POST"])
        self.router.add_api_route("/favorites/{game_id}", self.delete_favorite, methods=["DELETE"])

    def get_favorite(self, current_user_id: int = Depends(get_current_user)):
        return self.actions_service.get_favorite(current_user_id)

    def add_favorite(self, game_id: int, current_user_id: int = Depends(get_current_user)):
        return self.actions_service.add_favorite(current_user_id, game_id)

    def delete_favorite(self, game_id: int, current_user_id: int = Depends(get_current_user)):
        return self.actions_service.delete_favorite(current_user_id, game_id)