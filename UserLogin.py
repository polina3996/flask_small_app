from flask import url_for
from flask_login import UserMixin


class UserLogin(UserMixin):
    def fromDB(self, user_id, db):
        """Taking a user from a database"""
        self.__user = db.get_user(user_id)
        return self

    def create(self, user):
        """Creating a new user"""
        self.__user = user
        return self

    def get_id(self):
        """a method that returns a unique identifier for the user as a string"""
        return str(self.__user['id'])

    def get_name(self):
        return self.__user['name'] if self.__user else 'Без имени'

    def get_email(self):
        return self.__user['email'] if self.__user else 'Без email'

    # def get_avatar(self, app):
    #     img = None
    #     if not self.__user['avatar']:
    #         try:
    #             with app.open_resource(app.root_path + url_for('static', filename='images/default.png'), 'rb') as f:
    #                 img = f.read()
    #         except FileNotFoundError as e:
    #             print('Не найден аватар по умолчанию: ' + str(e))
    #     else:
    #         img = self.__user['avatar']
    #     return img

    def verify_ext(self, filename):
        ext = filename.rsplit('.', 1)[1]
        if ext == 'png' or ext == 'PNG':
            return True
        return False

    # already exist in UserMixin

    # @property
    # def is_active(self):
    #"""a property that is True if the user's account is active or False otherwise."""
    #     return True
    #
    # @property
    # def is_authenticated(self):
    #"""a property that is True if the user has valid credentials or False otherwise."""
    #     return self.is_active
    #
    # @property
    # def is_anonymous(self):
    #"""a property that is False for regular users, and True for a special, anonymous user."""
    #     return False

