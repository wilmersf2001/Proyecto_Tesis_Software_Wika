from database.query.DataBase import Database
from datetime import datetime

db = Database()


def aumentar_correctas_progress(user_id, item_id):
    registro = db.check_record_exists(user_id, item_id)
    fecha_actual = datetime.now().date()
    fecha_actual_str = fecha_actual.strftime('%Y-%m-%d')

    if registro:
        query = "UPDATE tb_progress SET correctas = correctas + 1 WHERE user_id = ? AND item_id = ?"
        db.cursor.execute(query, (user_id, item_id))
        db.connection.commit()
    else:
        query = "INSERT INTO tb_progress (fecha_aprendizaje, user_id, item_id, correctas, incorrectas) VALUES (?, ?, ?, 1, 0)"
        db.cursor.execute(query, (fecha_actual_str, user_id, item_id))
        db.connection.commit()


def aumentar_incorrectas_progress(user_id, item_id):
    registro = db.check_record_exists(user_id, item_id)
    fecha_actual = datetime.now().date()
    fecha_actual_str = fecha_actual.strftime('%Y-%m-%d')

    if registro:
        query = "UPDATE tb_progress SET incorrectas = incorrectas + 1 WHERE user_id = ? AND item_id = ?"
        db.cursor.execute(query, (user_id, item_id))
        db.connection.commit()
    else:
        query = "INSERT INTO tb_progress (fecha_aprendizaje, user_id, item_id, correctas, incorrectas) VALUES (?, ?, ?, 0, 1)"
        db.cursor.execute(query, (fecha_actual_str, user_id, item_id))
        db.connection.commit()


def get_progress_user_by_category(user_id, category_id):
    total_category = db.get_cant_items_by_category(category_id)
    progress = db.get_progress_by_user_and_category(user_id, category_id)
    result = round(progress / total_category * 100,
                   2) if total_category > 0 else 0
    return result


def get_progress_by_user(user_id):
    total = db.get_all_items()
    progress = db.get_progress_by_user(user_id)
    result = round(progress / total * 100, 2) if total > 0 else 0
    return result


def get_all_progress_by_user_and_category(user_id, category_id):
    return db.get_all_progress_by_user_and_category(user_id, category_id)


def exist_parameter_in_progress_user(user_id, item_id):
    if db.check_record_exists(user_id, item_id):
        return True
    return False
