import sqlite3
from flask import g, flash
from flask_login import current_user
from datetime import datetime


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_restaurant(self, rest_id):
        """Takes a restaurant from the database by its id"""
        try:
            self.__cur.execute(f'SELECT * FROM restaurants WHERE id = {rest_id} LIMIT 1')
            res = self.__cur.fetchone()
            if not res:
                print('Ресторан не найден')
                return False
            return res
        except sqlite3.Error as e:
            print('Ошибка получения данных из БД' + str(e))
            raise e

    def add_user(self, username, email, hpsw):
        """Adds a user to the database"""
        try:
            self.__cur.execute(
                f'SELECT COUNT() as "count" FROM users WHERE email LIKE "{email}"')
            res_email = self.__cur.fetchone()
            if res_email['count'] > 0:
                print('Пользователь с таким email уже существует')
                return False
            self.__cur.execute(
                f'SELECT COUNT() as "count" FROM users WHERE username = {username}')
            res_name = self.__cur.fetchone()
            if res_name['count'] > 0:
                print('Пользователь с таким именем уже существует')
                return False
            self.__cur.execute('''INSERT INTO users VALUES(NULL, ?, ?, ?, NULL)''', (username, email, hpsw))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка добавления пользователя в БД' + str(e))
            raise e
        return True

    def get_user(self, user_id):
        """Takes a user from the database by his id"""
        try:
            self.__cur.execute(f'SELECT * FROM users WHERE id = {user_id} LIMIT 1')
            res = self.__cur.fetchone()
            if not res:
                print('Пользователь не найден')
                return False
            return res
        except sqlite3.Error as e:
            print('Ошибка получения данных из БД' + str(e))
            raise e

    def get_user_by_name(self, username):
        """Takes a user from the database by his name"""
        try:
            self.__cur.execute(f'SELECT * FROM users WHERE username = "{username}" LIMIT 1')
            res = self.__cur.fetchone()
            if not res:
                print('Пользователь не найден')
                return False
            return res
        except sqlite3.Error as e:
            print('Ошибка получения данных из БД ' + str(e))
            raise e

    def add_feedback(self, title, body, rest_id):
        """Adds the feedback to the database"""
        try:
            author_id = g.user['id']  # current_user.get_id()
            created = datetime.now()
            self.__cur.execute('''INSERT INTO feedbacks VALUES(NULL, ?, ?, ?, ?, ?)''',
                               (author_id, rest_id, title, body, created))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка добавления отзыва в БД' + str(e))
        return True

    def get_feedbacks_of_a_user(self, username):
        """Takes all feedbacks of the user"""
        try:
            self.__cur.execute(f"SELECT f.id, f.title, r.title AS rest_title, f.created, f.body, f.rest_id FROM "
                               f"restaurants AS r "
                               f"JOIN feedbacks AS f ON r.id = f.rest_id "
                               f" JOIN users AS u ON f.author_id=u.id "
                               f" WHERE u.username = '{username}' ORDER "
                               f"BY created DESC")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print('Ошибка получения отзывов из БД' + str(e))
        return []

    def get_feedback(self, feedback_id):
        """One feedback is taken from the database"""
        try:
            self.__cur.execute(f"SELECT u.username, f.author_id, f.title, f.body, f.created, r.title AS restaurant, "
                               f"f.rest_id "
                               f"FROM users AS u JOIN feedbacks AS f ON u.id = f.author_id "
                               f"JOIN restaurants AS r ON f.rest_id = r.id WHERE f.id = {feedback_id} LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print('Ошибка получения отзыва из БД' + str(e))
        return ()

    def get_feedbacks_of_a_restaurant(self, rest_id):
        """All feedbacks for the restaurant are taken from the database"""
        try:
            self.__cur.execute(f"SELECT f.id, f.title, u.username AS author, f.created, "
                               f"f.body, f.author_id FROM restaurants AS r "
                               f"JOIN feedbacks AS f ON f.rest_id=r.id "
                               f"JOIN users AS u ON u.id=f.author_id "
                               f"WHERE f.rest_id = {rest_id} "
                               f"ORDER BY created DESC")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print('Ошибка получения статьи из БД' + str(e))
            raise e
        return []

    def update_my_feedback(self, feedback_id, new_title, new_body):
        try:
            self.__cur.execute(f'''UPDATE feedbacks SET title = ? WHERE id = ?''', (new_title, feedback_id))
            self.__cur.execute(f'''UPDATE feedbacks SET body = ? WHERE id = ?''', (new_body, feedback_id))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка обновления отзыва в БД: ' + str(e))
            return False
        return True

    def delete_my_feedback(self, feedback_id):
        """Deletes a user's feedback"""
        try:
            self.__cur.execute(f'DELETE FROM feedbacks WHERE id = ?', (feedback_id,))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка удаления отзыва в БД: ' + str(e))
            return False
        return True

    def update_user_avatar(self, avatar, user_id):
        """Updates user's avatar in the database"""
        if not avatar:
            return False
        try:
            binary = sqlite3.Binary(avatar)
            self.__cur.execute(f'''UPDATE users SET avatar = ? WHERE id = ?''', (binary, user_id))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка обновления аватара в БД: ' + str(e))
            return False
        return True
