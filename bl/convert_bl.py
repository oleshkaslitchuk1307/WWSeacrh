from domain.interfaces.service_interfaces import IConvertService

class ConvertService(IConvertService):
    def game_to_dict(self, row) -> dict | None:
        if row is None:
            return None
        return {
            "id": row[0],
            "title": row[1],
            "genre": row[2],
            "rating": row[3],
            "image_url": row[4]
        }

    def games_to_list(self, rows) -> list:
        return [self.game_to_dict(row) for row in rows]

    def user_to_dict(self, row) -> dict | None:
        if row is None:
            return None
        return {
            "id": row[0],
            "username": row[1],
            "email": row[2],
            "avatar_url": row[4],
            "favorite_genre": row[5],
            "created_at": row[6]
        }

    def users_to_list(self, rows) -> list:
        return [self.user_to_dict(row) for row in rows]

    def message_to_dict(self, row) -> dict | None:
        if row is None:
            return None
        return {
            "id": row[0],
            "sender_id": row[1],
            "receiver_id": row[2],
            "message": row[3],
            "timestamp": row[4]
        }

    def messages_to_list(self, rows) -> list:
        return [self.message_to_dict(row) for row in rows]