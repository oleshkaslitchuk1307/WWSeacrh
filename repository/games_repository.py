from data_base import get_connection
from domain.interfaces.repository_interfaces import IGamesRepository

class GamesRepository(IGamesRepository):
    def get_all_games(self):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM games')
            return cursor.fetchall()
        finally:
            connection.close()

    def get_game_by_id(self, game_id: int):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM games WHERE id = ?', (game_id,))
            return cursor.fetchone()
        finally:
            connection.close()

    def create_game(self, game_data: dict):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO games(title, genre, rating, image_url) VALUES (?,?,?,?)', (game_data['title'], game_data['genre'], game_data['rating'], game_data['image_url']))
            connection.commit()
        finally:
            connection.close()

    def delete_game(self, game_id: int):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute('DELETE FROM games WHERE id = ?', (game_id,))
            connection.commit()
        finally:
            connection.close()

    def update_game(self, game_id: int, game_data: dict):
        if not game_data:
            return
        
        connection = get_connection()
        try:
            cursor = connection.cursor()
            fields = []
            values = []
            
            for key in ['title', 'genre', 'rating', 'image_url']:
                if key in game_data and game_data[key] is not None:
                    fields.append(f"{key} = ?")
                    values.append(game_data[key])
                    
            if not fields:
                return
                
            values.append(game_id)
            query = f"UPDATE games SET {', '.join(fields)} WHERE id = ?"
            cursor.execute(query, values)
            connection.commit()
        finally:
            connection.close()

    def search_games(self, title = None, genre = None, min_rating = None, max_rating = None, sort_by = 'rating', sort_order = 'desc'):
        connection = get_connection()
        try:
            cursor = connection.cursor()

            query = 'SELECT * FROM games WHERE 1=1'
            params = []

            if title:
                query += '  AND title LIKE ?'
                params.append(f'%{title}%')
            if genre:
                query += '  AND genre LIKE ?'
                params.append(genre)
            if min_rating:
                query += '  AND rating >= ?'
                params.append(min_rating)
            if max_rating:
                query += '  AND rating <= ?'
                params.append(max_rating)

            allowed_sort_fields = {'id', 'title', 'genre', 'rating'}
            sort_field = sort_by if sort_by in allowed_sort_fields else 'rating'
            order = 'ASC' if str(sort_order).lower() == 'asc' else 'DESC'
            query += f' ORDER BY {sort_field} {order}'
            cursor.execute(query, params)
            return cursor.fetchall()
        finally:
            connection.close()


    def get_distinct_genres(self):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT DISTINCT genre
                FROM games
                WHERE genre IS NOT NULL AND TRIM(genre) != ''
                ORDER BY genre ASC
                """
            )
            return [row[0] for row in cursor.fetchall()]
        finally:
            connection.close()
