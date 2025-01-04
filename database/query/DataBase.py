import sqlite3
from utils.Constants import Constants


class Database:

    def __init__(self):
        self.connection = sqlite3.connect(Constants.URL_DATABASE)
        self.cursor = self.connection.cursor()

    def get_id(self, table, id):
        self.cursor.execute(f'SELECT * FROM {table} WHERE id = {id}')
        return self.cursor.fetchone()

    def get_all(self, table):
        self.cursor.execute(f'SELECT * FROM {table}')
        return self.cursor.fetchall()

    def get_items_by_category(self, category_id):
        query = """
            SELECT tb_items.id, tb_items.nombre, tb_category.nombre, tb_category.id
            FROM tb_items
            INNER JOIN tb_category ON tb_items.category_id = tb_category.id
            WHERE tb_category.id = ?
        """
        self.cursor.execute(query, (category_id,))
        return self.cursor.fetchall()

    def get_cant_items_by_category(self, category_id):
        query = """
            SELECT COUNT(*) FROM tb_items WHERE category_id = ?
        """
        self.cursor.execute(query, (category_id,))
        return self.cursor.fetchone()[0]

    def get_all_items(self):
        query = """
            SELECT COUNT(*) FROM tb_items
        """
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def check_record_exists(self, user_id, item_id):
        query = "SELECT * FROM tb_progress WHERE user_id = ? AND item_id = ?"
        self.cursor.execute(query, (user_id, item_id))
        result = self.cursor.fetchone()
        return result if result else 0

    def get_progress_by_user_and_category(self, user_id, category_id):
        query = """
            SELECT COUNT(*)
            FROM tb_progress
            INNER JOIN tb_items ON tb_progress.item_id = tb_items.id
            INNER JOIN tb_category ON tb_items.category_id = tb_category.id
            WHERE tb_progress.user_id = ? AND tb_category.id = ?
        """
        self.cursor.execute(query, (user_id, category_id))
        return self.cursor.fetchone()[0]

    def get_all_progress_by_user_and_category(self, user_id, category_id):
        query = """
            SELECT tb_progress.fecha_aprendizaje, tb_items.nombre, tb_progress.correctas, tb_progress.incorrectas
            FROM tb_progress
            INNER JOIN tb_items ON tb_progress.item_id = tb_items.id
            INNER JOIN tb_category ON tb_items.category_id = tb_category.id
            WHERE tb_progress.user_id = ? AND tb_category.id = ?
        """
        self.cursor.execute(query, (user_id, category_id))
        return self.cursor.fetchall()

    def get_progress_by_user(self, user_id):
        query = """
            SELECT COUNT(*)
            FROM tb_progress
            WHERE user_id = ?
        """
        self.cursor.execute(query, (user_id,))
        return self.cursor.fetchone()[0]

    def delete_progress_by_user(self, user_id):
        query = """
            DELETE FROM tb_progress WHERE user_id = ?
        """
        self.cursor.execute(query, (user_id,))
        self.commit()

    def get_user_auth(self):
        self.cursor.execute("SELECT * FROM tb_user WHERE is_authenticated = 1")
        return self.cursor.fetchone()

    def logout_user(self):
        query = """
            UPDATE tb_user SET is_authenticated = 0
        """
        self.cursor.execute(query)
        self.commit()

    def update_user_auth(self, username):
        query_specific_user = """
        UPDATE tb_user SET is_authenticated = 1 WHERE username = ?
        """
        self.cursor.execute(query_specific_user, (username,))

        query_other_users = """
            UPDATE tb_user SET is_authenticated = 0 WHERE username != ?
        """
        self.cursor.execute(query_other_users, (username,))
        self.commit()

    def insert_user(self, username):
        query = """
            INSERT INTO tb_user (username, is_authenticated) VALUES (?, 0)
        """
        self.cursor.execute(query, (username,))
        self.commit()

    def delete_user(self, user_id):
        query = """
            DELETE FROM tb_user WHERE user_id = ?
        """
        self.cursor.execute(query, (user_id,))
        self.commit()

    def exist_id_item_in_progress_user(self, user_id, item_id):
        query = """
            SELECT * FROM tb_progress WHERE user_id = ? AND item_id = ?
        """
        self.cursor.execute(query, (user_id, item_id))
        return self.cursor.fetchone()

    def rollback(self):
        self.connection.rollback()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.close()
