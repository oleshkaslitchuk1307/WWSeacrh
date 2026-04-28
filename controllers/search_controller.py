from fastapi import APIRouter
from typing import Optional
from domain.interfaces.service_interfaces import ISearchService

class SearchController:
    def __init__(self, search_service: ISearchService):
        self.router = APIRouter(prefix="/search", tags=["search"])
        self.search_service = search_service
        self.setup_routes()

    def setup_routes(self):
        self.router.add_api_route("", self.search_game, methods=["GET"])

    def search_game(
        self,
        title: Optional[str] = None,
        genre: Optional[str] = None,
        min_rating: Optional[float] = None,
        max_rating: Optional[float] = None,
        sort_by: Optional[str] = "rating",
        sort_order: Optional[str] = "desc"
    ):
        return self.search_service.search_game(title, genre, min_rating, max_rating, sort_by, sort_order)