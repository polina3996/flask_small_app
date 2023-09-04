import sqlite3
from flask import g
from flask_login import current_user
from datetime import datetime


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

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
                print('Пользователь с таким email уже существует')
                return False
            self.__cur.execute('''INSERT INTO users VALUES(NULL, ?, ?, ?, NULL)''', (username, email, hpsw))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка добавления пользователя в БД' + str(e))
            return False
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
            print(res, flush=True)
            if not res:
                print('Пользователь не найден')
                return False
            return res
        except sqlite3.Error as e:
            print('Ошибка получения данных из БД ' + str(e))
        return False

    def add_feedback(self, title, body, rest_id):
        """Adds the feedback to the database"""
        try:
            author_id = g.user['id']  # current_user.get_id()
            created = datetime.now()
            self.__cur.execute('''INSERT INTO feedbacks VALUES(NULL, ?, ?, ?, ?, ?)''',
                               (author_id, rest_id, title, body, created))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка добавления статьи в БД' + str(e))
            raise e
        return True

    def get_feedbacks_of_a_user(self, user_id):
        """Takes all feedbacks of the user"""
        try:
            self.__cur.execute(f"SELECT f.id, f.title, r.title AS rest_title, f.created, f.body FROM feedbacks AS f "
                               f"JOIN restaurants AS r ON r.id = f.rest_id WHERE f.author_id = {user_id} ORDER "
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
            self.__cur.execute(f"SELECT u.username, r.id, f.title, f.body, f.created FROM feedbacks AS f JOIN users "
                               f"as u ON u.id=f.author_id JOIN restaurants as r ON f.rest_d=r.id WHERE f.id = {feedback_id}  LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print('Ошибка получения отзыва из БД' + str(e))
        return (False, False)

    # def get_feedbacks_anonce(self):
    #     try:
    #         self.__cur.execute(f"SELECT * FROM feedbacks ORDER BY created DESC")
    #         res = self.__cur.fetchall()
    #         if res:
    #             return res
    #     except sqlite3.Error as e:
    #         print('Ошибка получения статьи из БД' + str(e))
    #     return []

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
