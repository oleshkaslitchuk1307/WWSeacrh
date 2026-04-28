from repository.games_repository import GamesRepository
from repository.user_repository import UserRepository
from repository.chat_repository import ChatRepository
from repository.favorites_repository import FavoritesRepository
from bl.games_bl import GameService
from bl.user_bl import UserService
from bl.auth_bl import AuthService
from bl.chat_bl import ChatService
from bl.actions_bl import ActionsService
from bl.search_bl import SearchService
from bl.sharing_bl import SharingService
from bl.validation_bl import ValidationService
from bl.convert_bl import ConvertService
from bl.jwt_bl import JWTService
from controllers.games_controller import GamesController
from controllers.user_controller import UserController
from controllers.auth_controller import AuthController
from controllers.chat_controller import ChatController
from controllers.actions_controller import ActionsController
from controllers.search_controller import SearchController
from controllers.sharing_controller import SharingController

class Container:
    def __init__(self):
        # Repositories
        self.games_repository = GamesRepository()
        self.user_repository = UserRepository()
        self.chat_repository = ChatRepository()
        self.favorites_repository = FavoritesRepository()

        # Low-level Services
        self.validation_service = ValidationService()
        self.convert_service = ConvertService()
        self.jwt_service = JWTService()
        self.sharing_service = SharingService()

        # Business Logic Services
        self.games_service = GameService(
            self.games_repository, 
            self.validation_service, 
            self.convert_service
        )
        self.user_service = UserService(
            self.user_repository, 
            self.validation_service, 
            self.convert_service
        )
        self.auth_service = AuthService(
            self.user_repository, 
            self.validation_service, 
            self.convert_service, 
            self.jwt_service
        )
        self.chat_service = ChatService(
            self.chat_repository, 
            self.convert_service
        )
        self.actions_service = ActionsService(
            self.favorites_repository, 
            self.convert_service
        )
        self.search_service = SearchService(
            self.games_repository, 
            self.convert_service
        )

        # Controllers
        self.games_controller = GamesController(self.games_service)
        self.user_controller = UserController(self.user_service)
        self.auth_controller = AuthController(self.auth_service)
        self.chat_controller = ChatController(self.chat_service)
        self.actions_controller = ActionsController(self.actions_service)
        self.search_controller = SearchController(self.search_service)
        self.sharing_controller = SharingController(self.sharing_service)
