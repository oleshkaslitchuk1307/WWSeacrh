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

from domain.interfaces.repository_interfaces import (
    IGamesRepository, IUserRepository, IChatRepository, IFavoritesRepository
)
from domain.interfaces.service_interfaces import (
    IGameService, IUserService, IAuthService, IChatService, 
    IActionsService, ISearchService, ISharingService, 
    IValidationService, IConvertService, IJWTService
)

class Container:
    def __init__(self):
        self._storage = {}
        
        # Repositories
        self._storage[IGamesRepository] = GamesRepository()
        self._storage[IUserRepository] = UserRepository()
        self._storage[IChatRepository] = ChatRepository()
        self._storage[IFavoritesRepository] = FavoritesRepository()
        
        # Base Services
        self._storage[IValidationService] = ValidationService()
        self._storage[IConvertService] = ConvertService()
        self._storage[IJWTService] = JWTService()
        self._storage[ISharingService] = SharingService()
        
        # Business Logic Services
        self._storage[IGameService] = GameService(
            self._storage[IGamesRepository], 
            self._storage[IValidationService], 
            self._storage[IConvertService]
        )
        self._storage[IUserService] = UserService(
            self._storage[IUserRepository], 
            self._storage[IValidationService], 
            self._storage[IConvertService]
        )
        self._storage[IAuthService] = AuthService(
            self._storage[IUserRepository], 
            self._storage[IValidationService], 
            self._storage[IConvertService], 
            self._storage[IJWTService]
        )
        self._storage[IChatService] = ChatService(
            self._storage[IChatRepository], 
            self._storage[IConvertService]
        )
        self._storage[IActionsService] = ActionsService(
            self._storage[IFavoritesRepository], 
            self._storage[IConvertService]
        )
        self._storage[ISearchService] = SearchService(
            self._storage[IGamesRepository], 
            self._storage[IConvertService]
        )

        # Controllers
        self._games_controller = GamesController(self._storage[IGameService])
        self._user_controller = UserController(self._storage[IUserService])
        self._auth_controller = AuthController(self._storage[IAuthService])
        self._chat_controller = ChatController(self._storage[IChatService])
        self._actions_controller = ActionsController(self._storage[IActionsService])
        self._search_controller = SearchController(self._storage[ISearchService])
        self._sharing_controller = SharingController(self._storage[ISharingService])

    @property
    def games_controller(self): return self._games_controller
    
    @property
    def user_controller(self): return self._user_controller
    
    @property
    def auth_controller(self): return self._auth_controller
    
    @property
    def chat_controller(self): return self._chat_controller
    
    @property
    def actions_controller(self): return self._actions_controller
    
    @property
    def search_controller(self): return self._search_controller
    
    @property
    def sharing_controller(self): return self._sharing_controller
