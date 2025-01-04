from database.query.DataBase import Database

db = Database()


def get_all_categories():
    return db.get_all('tb_category')
