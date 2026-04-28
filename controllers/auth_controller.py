from fastapi import APIRouter, Depends
from domain.models.view_models.user_vm import UserRegister, UserLogin
from bl.jwt_bl import oauth2_scheme
from domain.interfaces.service_interfaces import IAuthService

class AuthController:
    def __init__(self, auth_service: IAuthService):
        self.router = APIRouter(prefix="/auth", tags=["auth"])
        self.auth_service = auth_service
        self.setup_routes()

    def setup_routes(self):
        self.router.add_api_route("/register", self.register, methods=["POST"])
        self.router.add_api_route("/login", self.login, methods=["POST"])
        self.router.add_api_route("/logout", self.logout, methods=["POST"])

    def register(self, user: UserRegister):
       return self.auth_service.register(user)

    def login(self, user: UserLogin):
        return self.auth_service.login(user)

    def logout(self, token: str = Depends(oauth2_scheme)):
        return self.auth_service.logout(token)