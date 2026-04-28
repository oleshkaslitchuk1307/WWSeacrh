from abc import ABC, abstractmethod

class IGamesRepository(ABC):
    @abstractmethod
    def get_all_games(self):
        pass

    @abstractmethod
    def get_game_by_id(self, game_id: int):
        pass

    @abstractmethod
    def create_game(self, game_data: dict):
        pass

    @abstractmethod
    def delete_game(self, game_id: int):
        pass

    @abstractmethod
    def update_game(self, game_id: int, game_data: dict):
        pass

    @abstractmethod
    def search_games(self, title=None, genre=None, min_rating=None, max_rating=None, sort_by='rating', sort_order='desc'):
        pass

    @abstractmethod
    def get_distinct_genres(self):
        pass

class IUserRepository(ABC):
    @abstractmethod
    def get_user_by_id(self, user_id: int):
        pass

    @abstractmethod
    def create_user(self, user_data):
        pass

    @abstractmethod
    def delete_user(self, user_id: int):
        pass

    @abstractmethod
    def get_user_by_username(self, username: str):
        pass

    @abstractmethod
    def update_user(self, user_id: int, user_data: dict):
        pass

    @abstractmethod
    def search_users_by_username(self, query: str, current_user_id: int, limit: int = 20):
        pass

    @abstractmethod
    def add_friend(self, sender_id: int, receiver_id: int):
        pass

    @abstractmethod
    def get_friends(self, user_id: int):
        pass

    @abstractmethod
    def accept_friend(self, receiver_id: int, sender_id: int):
        pass

    @abstractmethod
    def reject_friend(self, receiver_id: int, sender_id: int):
        pass

    @abstractmethod
    def remove_friend(self, user_id: int, friend_id: int):
        pass

class IChatRepository(ABC):
    @abstractmethod
    def create_message(self, message_data: dict):
        pass

    @abstractmethod
    def get_messages_between_users(self, user1_id: int, user2_id: int):
        pass

    @abstractmethod
    def get_dialog_partners(self, user_id: int):
        pass

class IFavoritesRepository(ABC):
    @abstractmethod
    def get_favorites(self, user_id: int):
        pass

    @abstractmethod
    def add_favorite(self, user_id: int, game_id: int):
        pass

    @abstractmethod
    def delete_favorite(self, user_id: int, game_id: int):
        pass
