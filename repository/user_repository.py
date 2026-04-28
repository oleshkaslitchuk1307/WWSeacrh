from data_base import get_connection
from domain.interfaces.repository_interfaces import IUserRepository

class UserRepository(IUserRepository):
    def get_user_by_id(self, user_id: int):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id, username, email, password, avatar_url, favorite_genre, created_at
                FROM users
                WHERE id = ?
                """,
                (user_id,)
            )
            return cursor.fetchone()
        finally:
            connection.close()

    def create_user(self, user_data):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                           (user_data['username'], user_data['email'], user_data['password']))
            connection.commit()
        finally:
            connection.close()

    def delete_user(self, user_id: int):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            connection.commit()
        finally:
            connection.close()

    def get_user_by_username(self, username: str):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id, username, email, password, avatar_url, favorite_genre, created_at
                FROM users
                WHERE username = ?
                """,
                (username,)
            )
            return cursor.fetchone()
        finally:
            connection.close()

    def update_user(self, user_id: int, user_data: dict):
        if not user_data:
            return
        connection = get_connection()
        try:
            cursor = connection.cursor()
            fields = []
            values = []
            if 'username' in user_data:
                fields.append("username = ?")
                values.append(user_data['username'])
            if 'email' in user_data:
                fields.append("email = ?")
                values.append(user_data['email'])
            if 'password' in user_data:
                fields.append("password = ?")
                values.append(user_data['password'])
            if 'avatar_url' in user_data:
                fields.append("avatar_url = ?")
                values.append(user_data['avatar_url'])
            if 'favorite_genre' in user_data:
                fields.append("favorite_genre = ?")
                values.append(user_data['favorite_genre'])
            if not fields:
                return
            values.append(user_id)
            query = f"UPDATE users SET {', '.join(fields)} WHERE id = ?"
            cursor.execute(query, values)
            connection.commit()
        finally:
            connection.close()

    def search_users_by_username(self, query: str, current_user_id: int, limit: int = 20):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            like_value = f"%{query}%"
            cursor.execute(
                """
                SELECT id, username, avatar_url
                FROM users
                WHERE username LIKE ? AND id != ?
                ORDER BY username ASC
                LIMIT ?
                """,
                (like_value, current_user_id, limit)
            )
            return cursor.fetchall()
        finally:
            connection.close()

    def add_friend(self, sender_id: int, receiver_id: int):
        if sender_id == receiver_id:
            raise ValueError("Неможливо додати себе в друзі")
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO friends (sender_id, receiver_id, status) VALUES (?, ?, 'pending')",
                (sender_id, receiver_id)
            )
            connection.commit()
        finally:
            connection.close()

    def get_friends(self, user_id: int):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT
                    u.id,
                    u.username,
                    u.avatar_url,
                    f.status,
                    CASE WHEN f.sender_id = ? THEN 'sent' ELSE 'received' END as direction
                FROM friends f
                JOIN users u ON u.id = CASE
                    WHEN f.sender_id = ? THEN f.receiver_id
                    ELSE f.sender_id
                END
                WHERE f.sender_id = ? OR f.receiver_id = ?
                ORDER BY u.username ASC
                """,
                (user_id, user_id, user_id, user_id)
            )
            return cursor.fetchall()
        finally:
            connection.close()

    def accept_friend(self, receiver_id: int, sender_id: int):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE friends SET status = 'accepted' WHERE sender_id = ? AND receiver_id = ?",
                (sender_id, receiver_id)
            )
            connection.commit()
        finally:
            connection.close()

    def reject_friend(self, receiver_id: int, sender_id: int):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM friends WHERE sender_id = ? AND receiver_id = ?",
                (sender_id, receiver_id)
            )
            connection.commit()
        finally:
            connection.close()

    def remove_friend(self, user_id: int, friend_id: int):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                "DELETE FROM friends WHERE (sender_id = ? AND receiver_id = ?) OR (sender_id = ? AND receiver_id = ?)",
                (user_id, friend_id, friend_id, user_id)
            )
            connection.commit()
        finally:
            connection.close()
