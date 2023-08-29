import functools
import os
import sqlite3
from flask import Flask, render_template, session, url_for, request, flash, redirect, g, make_response
from flask_login import login_required, current_user, LoginManager

from FDataBase import FDataBase
from UserLogin import UserLogin
from db import get_db
from instance.config import SECRET_KEY


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY=SECRET_KEY, DATABASE=os.path.join(app.instance_path, 'flask_small_app.sqlite'))
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.errorhandler(404)
    def page_not_found(error):
        """Page not found handler"""
        return render_template('page404.html')

    @app.route('/')
    @app.route('/index')
    def index():
        """Main page handler"""
        return render_template('index.html')

    @app.route('/gourmand')
    def gourmand():
        """Restaurant 'Gourmand' page handler"""
        return render_template('gourmand.html')

    @app.route('/alaverdi')
    def alaverdi():
        """Restaurant 'Alaverdi' page handler"""
        return render_template('alaverdi.html')

    @app.route('/heart_of_batumi')
    def heart_of_batumi():
        """Restaurant 'Heart of Batumi' page handler"""
        return render_template('heart_of_batumi.html')

    @app.route('/panorama')
    def panorama():
        """Restaurant 'Panorama' page handler"""
        return render_template('panorama.html')

    @app.route('/tavaduri')
    def tavaduri():
        """Restaurant 'Tavaduri' page handler"""
        return render_template('tavaduri.html')

    @app.route('/mangal')
    def mangal():
        """Restaurant 'Mangal' page handler"""
        return render_template('mangal.html')

    # @app.route('/restaurant/<alias>')
    # def restaurant(alias):
    #     """Restaurant page handler"""
    #     title, url = dbase.get_restaurant(alias)
    #     if not title:
    #         abort(404)
    #     return render_template('restaurant.html', menu=dbase.get_menu(), title=title, post=post)

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login'  # при посещении закрытой страницы(только для авторизованных) будет открываться страница с авторизацией
    login_manager.login_message = 'Авторизуйтесь для доступа к закрытым страницам'  # задаем новое мгновенное сообщение
    login_manager.login_message_category = 'success'

    # id передается в запросе к серверу(в конкр сессии)
    @login_manager.user_loader  # вызывается после before_query(где устанавливается связь с БД)
    def load_user(user_id):  # +
        return UserLogin().fromDB(user_id,
                                  dbase)  # загружаем информ о юзере из БД и создаем ЭК -> понятно, какой пользователь сейчас авторизован

    @app.route('/profile')
    # @login_required
    def profile():
        """Opens a profile page only for authorized users"""
        return render_template('profile.html')

    def verify_ext(filename):
        """Verifies the extension of the file is 'png'"""
        ext = filename.rsplit('.', 1)[1]
        if ext == 'png' or ext == 'PNG':
            return True
        return False

    @app.route('/userava')
    # @login_required
    def userava():
        """Returns an image in PNG-format"""
        db = get_db()
        user = db.execute('''SELECT * FROM users WHERE id = ?''', (session.get('user_id'),)).fetchone()
        img = None
        if not user['avatar']:
            try:
                with open('flask_small_app/static/images/default.png', 'rb') as f:
                    print('Аватар найден')
                    img = f.read()
            except FileNotFoundError as e:
                print('Не найден аватар по умолчанию: ' + str(e))
            else:
                img = user['avatar']
        if not img:
            return ""
        resp = make_response(img)
        resp.headers['Content-Type'] = 'image/png'
        return resp

    @app.route('/upload', methods=['POST', 'GET'])
    # @login_required
    def upload():
        """Uploads an image into user's profile"""
        db = get_db()
        user = db.execute('''SELECT * FROM users WHERE id = ?''', (session.get('user_id'),)).fetchone()
        if request.method == 'POST':
            file = request.files['file']
            if file and verify_ext(file.filename):
                try:
                    img = file.read()
                    db.execute(f'UPDATE users SET avatar = ? WHERE id = ?', (sqlite3.Binary(img), user['id']))
                    db.commit()
                except sqlite3.Error as e:
                    flash('Ошибка обновления аватара', 'error')
                except FileNotFoundError as e:
                    flash('Ошибка чтения файла', 'error')
            else:
                flash('Ошибка обновления аватара', 'error')
        flash('Аватар обновлен', 'success')
        return redirect(url_for('profile'))

    import db, auth

    # initializing of database
    db.init_app(app)

    # registration of a blueprint 'auth.py'
    app.register_blueprint(auth.auth)

    return app
