from database.query.DataBase import Database

db = Database()


def get_user_auth():
    return db.get_user_auth()


def logout_user():
    return db.logout_user()


def delete_progress_by_user(user_id):
    return db.delete_progress_by_user(user_id)


def get_all_users():
    return db.get_all('tb_user')


def update_user_auth(username):
    return db.update_user_auth(username)


def insert_user(username):
    return db.insert_user(username)


def delete_user(user_id):
    return db.delete_user(user_id)
