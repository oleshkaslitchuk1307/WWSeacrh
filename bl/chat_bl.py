from domain.interfaces.repository_interfaces import IChatRepository
from domain.interfaces.service_interfaces import IChatService, IConvertService

class ChatService(IChatService):
    def __init__(self, chat_repository: IChatRepository, convert_service: IConvertService):
        self.chat_repository = chat_repository
        self.convert_service = convert_service

    def send_message(self, sender_id: int, message_data: dict):
        payload = {
            "sender_id": sender_id,
            "receiver_id": message_data["receiver_id"],
            "message": message_data["message"].strip()
        }
        if not payload["message"]:
            raise ValueError("Повідомлення не може бути порожнім")
        self.chat_repository.create_message(payload)
        return {"message": "Повідомлення надіслано"}

    def get_messages(self, user1_id: int, user2_id: int):
        rows = self.chat_repository.get_messages_between_users(user1_id, user2_id)
        return self.convert_service.messages_to_list(rows)

    def get_dialogs(self, user_id: int):
        rows = self.chat_repository.get_dialog_partners(user_id)
        return [
            {"id": row[0], "username": row[1], "avatar_url": row[2]}
            for row in rows
        ]