from database.query.DataBase import Database

db = Database()


def get_items_by_category(category):
    return db.get_items_by_category(category)
