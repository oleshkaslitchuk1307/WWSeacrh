import bcrypt
from domain.interfaces.repository_interfaces import IUserRepository
from domain.interfaces.service_interfaces import IUserService, IValidationService, IConvertService

class UserService(IUserService):
    def __init__(self, user_repository: IUserRepository, validation_service: IValidationService, convert_service: IConvertService):
        self.user_repository = user_repository
        self.validation_service = validation_service
        self.convert_service = convert_service

    def get_user(self, user_id: int):
        row = self.user_repository.get_user_by_id(user_id)
        return self.convert_service.user_to_dict(row)

    def update_user(self, user_id: int, user_data: dict):
        user_dict = user_data.model_dump(exclude_unset=True)
        self.validation_service.validate_user_update(user_dict)
        if 'password' in user_dict and user_dict['password'] is not None:
            hashed = bcrypt.hashpw(user_dict['password'].encode('utf-8'), bcrypt.gensalt())
            user_dict['password'] = hashed.decode('utf-8')
        return self.user_repository.update_user(user_id, user_dict)

    def delete_user(self, user_id: int):
        return self.user_repository.delete_user(user_id)

    def search_users(self, query: str, current_user_id: int):
        rows = self.user_repository.search_users_by_username(query.strip(), current_user_id)
        return [
            {"id": row[0], "username": row[1], "avatar_url": row[2]}
            for row in rows
        ]

    def add_friend(self, current_user_id: int, friend_id: int):
        if self.user_repository.get_user_by_id(friend_id) is None:
            raise ValueError("Користувача не знайдено")
        self.user_repository.add_friend(current_user_id, friend_id)
        return {"message": "Запит у друзі надіслано"}

    def accept_friend(self, current_user_id: int, friend_id: int):
        self.user_repository.accept_friend(current_user_id, friend_id)
        return {"message": "Запит у друзі прийнято"}

    def reject_friend(self, current_user_id: int, friend_id: int):
        self.user_repository.reject_friend(current_user_id, friend_id)
        return {"message": "Запит у друзі відхилено"}

    def remove_friend(self, current_user_id: int, friend_id: int):
        self.user_repository.remove_friend(current_user_id, friend_id)
        return {"message": "Користувача видалено з друзів"}

    def get_friends(self, current_user_id: int):
        rows = self.user_repository.get_friends(current_user_id)
        return [
            {
                "id": row[0],
                "username": row[1],
                "avatar_url": row[2],
                "status": row[3],
                "direction": row[4]
            }
            for row in rows
        ]