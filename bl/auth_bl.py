import bcrypt
from fastapi import HTTPException
from domain.interfaces.repository_interfaces import IUserRepository
from domain.interfaces.service_interfaces import IAuthService, IValidationService, IConvertService, IJWTService

class AuthService(IAuthService):
    def __init__(self, user_repository: IUserRepository, validation_service: IValidationService, convert_service: IConvertService, jwt_service: IJWTService):
        self.user_repository = user_repository
        self.validation_service = validation_service
        self.convert_service = convert_service
        self.jwt_service = jwt_service

    def register(self, user_data: dict):
        user_dict = user_data.model_dump()
        self.validation_service.validate_user(user_dict)
        hashed = bcrypt.hashpw(user_dict['password'].encode('utf-8'), bcrypt.gensalt())
        new_user = {
            'username': user_dict['username'],
            'password': hashed.decode('utf-8'),
            'email': user_dict['email'],
        }
        self.user_repository.create_user(new_user)
        return {"message": "Користувача зареєстровано"}

    def login(self, user_data: dict):
        user_dict = user_data.model_dump()
        user = self.user_repository.get_user_by_username(user_dict['username'])
        if user is None:
            raise HTTPException(status_code=401, detail="Невірний логін або пароль")
        if bcrypt.checkpw(user_dict['password'].encode('utf-8'), user[3].encode('utf-8')):
            token = self.jwt_service.create_token({'sub': str(user[0])})
            return {'access_token': token, 'token_type': 'bearer'}
        raise HTTPException(status_code=401, detail="Невірний логін або пароль")

    def logout(self, token: str):
        self.jwt_service.revoke_token(token)
        return {'повідомлення': 'Ви успішно вийшли з системи'}