from data_base import get_connection
from domain.interfaces.repository_interfaces import IFavoritesRepository

class FavoritesRepository(IFavoritesRepository):
    def get_favorites(self, user_id: int) -> list:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """SELECT g.id, g.title, g.genre, g.rating, g.image_url
                   FROM favorites f
                   JOIN games g ON f.game_id = g.id
                   WHERE f.user_id = ?""",
                (user_id,)
            )
            return cursor.fetchall()
        finally:
            connection.close()

    def add_favorite(self, user_id: int, game_id: int):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO favorites (user_id, game_id) VALUES (?, ?)', (user_id, game_id))
            connection.commit()
        finally:
            connection.close()

    def delete_favorite(self, user_id: int, game_id: int):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM favorites WHERE user_id = ? AND game_id = ?", (user_id, game_id))
            connection.commit()
        finally:
            connection.close()

