from domain.interfaces.repository_interfaces import IGamesRepository
from domain.interfaces.service_interfaces import ISearchService, IConvertService

class SearchService(ISearchService):
    def __init__(self, games_repository: IGamesRepository, convert_service: IConvertService):
        self.games_repository = games_repository
        self.convert_service = convert_service

    def search_game(self, title = None, genre = None, min_rating = None, max_rating = None, sort_by = 'rating', sort_order = 'desc'):
        rows = self.games_repository.search_games(title, genre, min_rating, max_rating, sort_by, sort_order)
        return self.convert_service.games_to_list(rows)