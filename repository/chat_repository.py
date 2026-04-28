from data_base import get_connection
from domain.interfaces.repository_interfaces import IChatRepository

class ChatRepository(IChatRepository):
    def create_message(self, message_data: dict):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                'INSERT INTO messages (sender_id, receiver_id, message) VALUES (?, ?, ?)',
                (message_data['sender_id'], message_data['receiver_id'], message_data['message'])
            )
            connection.commit()
        finally:
            connection.close()

    def get_messages_between_users(self, user1_id: int, user2_id: int):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                '''
                SELECT * FROM messages 
                WHERE (sender_id = ? AND receiver_id = ?) 
                   OR (sender_id = ? AND receiver_id = ?)
                ORDER BY timestamp ASC
                ''',
                (user1_id, user2_id, user2_id, user1_id)
            )
            return cursor.fetchall()
        finally:
            connection.close()


    def get_dialog_partners(self, user_id: int):
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT
                    u.id,
                    u.username,
                    u.avatar_url
                FROM (
                    SELECT DISTINCT
                        CASE
                            WHEN sender_id = ? THEN receiver_id
                            ELSE sender_id
                        END AS partner_id
                    FROM messages
                    WHERE sender_id = ? OR receiver_id = ?
                ) p
                JOIN users u ON u.id = p.partner_id
                ORDER BY u.username ASC
                """,
                (user_id, user_id, user_id)
            )
            return cursor.fetchall()
        finally:
            connection.close()

