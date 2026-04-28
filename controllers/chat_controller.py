from fastapi import APIRouter, Depends
from domain.models.view_models.chat_vm import MessageCreate
from bl.jwt_bl import get_current_user
from domain.interfaces.service_interfaces import IChatService

class ChatController:
    def __init__(self, chat_service: IChatService):
        self.router = APIRouter(prefix="/chat", tags=["chat"])
        self.chat_service = chat_service
        self.setup_routes()

    def setup_routes(self):
        self.router.add_api_route("", self.send_message, methods=["POST"])
        self.router.add_api_route("/dialogs", self.get_dialogs, methods=["GET"])
        self.router.add_api_route("/{other_user_id}", self.get_messages, methods=["GET"])

    def send_message(self, message: MessageCreate, current_user_id: int = Depends(get_current_user)):
        return self.chat_service.send_message(current_user_id, message.model_dump())

    def get_dialogs(self, current_user_id: int = Depends(get_current_user)):
        return self.chat_service.get_dialogs(current_user_id)

    def get_messages(self, other_user_id: int, current_user_id: int = Depends(get_current_user)):
        return self.chat_service.get_messages(current_user_id, other_user_id)
