from abc import ABC, abstractmethod

class IGameService(ABC):
    @abstractmethod
    def get_games(self):
        pass

    @abstractmethod
    def get_game_by_id(self, game_id: int):
        pass

    @abstractmethod
    def create_game(self, game):
        pass

    @abstractmethod
    def update_game(self, game_id: int, game):
        pass

    @abstractmethod
    def delete_game(self, game_id: int):
        pass

    @abstractmethod
    def get_genres(self):
        pass

class IAuthService(ABC):
    @abstractmethod
    def register(self, user_data: dict):
        pass

    @abstractmethod
    def login(self, user_data: dict):
        pass

    @abstractmethod
    def logout(self, token: str):
        pass

class IUserService(ABC):
    @abstractmethod
    def get_user(self, user_id: int):
        pass

    @abstractmethod
    def update_user(self, user_id: int, user_data: dict):
        pass

    @abstractmethod
    def delete_user(self, user_id: int):
        pass

    @abstractmethod
    def search_users(self, query: str, current_user_id: int):
        pass

    @abstractmethod
    def add_friend(self, current_user_id: int, friend_id: int):
        pass

    @abstractmethod
    def accept_friend(self, current_user_id: int, friend_id: int):
        pass

    @abstractmethod
    def reject_friend(self, current_user_id: int, friend_id: int):
        pass

    @abstractmethod
    def remove_friend(self, current_user_id: int, friend_id: int):
        pass

    @abstractmethod
    def get_friends(self, current_user_id: int):
        pass

class IChatService(ABC):
    @abstractmethod
    def send_message(self, sender_id: int, message_data: dict):
        pass

    @abstractmethod
    def get_messages(self, user1_id: int, user2_id: int):
        pass

    @abstractmethod
    def get_dialogs(self, user_id: int):
        pass

class IActionsService(ABC):
    @abstractmethod
    def add_favorite(self, user_id: int, game_id: int):
        pass

    @abstractmethod
    def delete_favorite(self, user_id: int, game_id: int):
        pass

    @abstractmethod
    def get_favorite(self, user_id: int):
        pass

class ISearchService(ABC):
    @abstractmethod
    def search_game(self, title=None, genre=None, min_rating=None, max_rating=None, sort_by='rating', sort_order='desc'):
        pass

class ISharingService(ABC):
    @abstractmethod
    def share_game(self, game_id: int):
        pass

class IValidationService(ABC):
    @abstractmethod
    def validate_game(self, game_data: dict):
        pass

    @abstractmethod
    def validate_user(self, user_data: dict):
        pass

    @abstractmethod
    def validate_user_update(self, user_data: dict):
        pass

class IConvertService(ABC):
    @abstractmethod
    def game_to_dict(self, row):
        pass

    @abstractmethod
    def games_to_list(self, rows):
        pass

    @abstractmethod
    def user_to_dict(self, row):
        pass

    @abstractmethod
    def users_to_list(self, rows):
        pass

    @abstractmethod
    def message_to_dict(self, row):
        pass

    @abstractmethod
    def messages_to_list(self, rows):
        pass

class IJWTService(ABC):
    @abstractmethod
    def create_token(self, data: dict):
        pass

    @abstractmethod
    def decode_token(self, token: str):
        pass

    @abstractmethod
    def revoke_token(self, token: str):
        pass

    @abstractmethod
    def is_token_revoked(self, token: str):
        pass
