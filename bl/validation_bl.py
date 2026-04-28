from domain.interfaces.service_interfaces import IValidationService

class ValidationService(IValidationService):
    def validate_game(self, game_data: dict):
        if not game_data.get('title'):
            raise ValueError("Назва гри не може бути порожньою")
        if game_data.get('rating') is not None and (game_data.get('rating') < 0 or game_data.get('rating') > 10):
            raise ValueError("Рейтинг гри має бути від 0 до 10")
        if not game_data.get('genre'):
            raise ValueError("Жанр гри не може бути порожнім")

    def validate_user(self, user_data: dict):
        if not user_data.get('username'):
            raise ValueError("Ім'я користувача не може бути порожнім")
        if not user_data.get('email'):
            raise ValueError("Email користувача не може бути порожнім")
        if '@' not in user_data.get('email'):
            raise ValueError("Email має містити @")
        if not user_data.get('password'):
            raise ValueError("Пароль користувача не може бути порожнім")
        if len(user_data.get('password')) < 6:
            raise ValueError("Пароль користувача має бути не менше 6 символів")

    def validate_user_update(self, user_data: dict):
        if user_data.get('email') is not None:
            if not user_data.get('email'):
                raise ValueError("Email користувача не може бути порожнім")
            if '@' not in user_data.get('email'):
                raise ValueError("Email має містити @")
        if user_data.get('password') is not None and len(user_data.get('password')) < 6:
            raise ValueError("Пароль користувача має бути не менше 6 символів")
        if user_data.get('avatar_url') is not None and len(user_data.get('avatar_url')) > 255:
            raise ValueError("Занадто довге посилання на аватар")