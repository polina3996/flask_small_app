import math
import sqlite3
import time

from flask_login import current_user


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def get_user(self, user_id):
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

    def add_post(self, title, body):
        try:
            author_id = current_user.get_id() #g.user['id']?
            created = math.floor(time.time())
            self.__cur.execute('''INSERT INTO feedbacks VALUES(NULL, ?, ?, ?, ?)''', (author_id, title, body, created))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка добавления статьи в БД' + str(e))
            return False
        return True

    # def get_post(self, alias):
    #     try:
    #         self.__cur.execute(f"SELECT title, text FROM posts WHERE url LIKE '{alias}'  LIMIT 1")
    #         res = self.__cur.fetchone()
    #         if res:
    #             return res
    #     except sqlite3.Error as e:
    #         print('Ошибка получения статьи из БД' + str(e))
    #     return (False, False)

    # def get_posts_anonce(self):
    #     try:
    #         self.__cur.execute(f"SELECT id, title, text, url FROM posts ORDER BY timee DESC")
    #         res = self.__cur.fetchall()
    #         if res:
    #             return res
    #     except sqlite3.Error as e:
    #         print('Ошибка получения статьи из БД' + str(e))
    #     return []

    def get_feedbacks_of_a_user(self, user_id):
        try:
            self.__cur.execute(f"SELECT title, body, url, created FROM feedbacks JOIN users ON users.id = "
                               f"feedbacks.author_id WHERE author_id = {user_id} ORDER BY created DESC")
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print('Ошибка получения отзывов из БД' + str(e))
        return []

    def add_user(self, username, email, hpsw):
        try:
            self.__cur.execute(
                f'SELECT COUNT() as "count" FROM users WHERE email LIKE "{email}"')
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print('Пользователь с таким email уже существует')
                return False
            self.__cur.execute('''INSERT INTO users VALUES(NULL, ?, ?, ?, NULL)''', (username, email, hpsw))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Ошибка добавления пользователя в БД' + str(e))
            return False
        return True

    def get_user_by_name(self, username):
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

    def update_user_avatar(self, avatar, user_id):
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