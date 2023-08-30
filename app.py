import os
import sqlite3
from datetime import datetime

from flask import Flask, render_template, session, url_for, request, flash, redirect, g, make_response
from flask_login import LoginManager
import db
from FDataBase import FDataBase
from UserLogin import UserLogin
from instance.config import SECRET_KEY
from auth import auth as auth_bp
from flask_login import current_user, login_required

login_manager = LoginManager()
# redirects to login page when trying to access must-be-authorized pages
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Авторизуйтесь для доступа к закрытым страницам'
login_manager.login_message_category = 'success'


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

    # initializing of database
    db.init_app(app)

    login_manager.init_app(app)

    # registration of a blueprint 'auth.py'
    app.register_blueprint(auth_bp)

    @login_manager.user_loader
    def load_user(user_id):
        """Runs a database query that will put the target user in the database session"""
        return UserLogin().fromDB(user_id, FDataBase(db.get_db()))  # int(user_id)??

    @app.before_request
    def before_request():
        """Sets the time a user was last seen in an application"""
        if current_user.is_authenticated:
            current_user.last_seen = datetime.utcnow()
            db.get_db().commit()

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

    @app.route('/profile/<username>')
    @login_required
    def profile(username):
        """Opens a profile page only for authorized users"""
        #user = FDataBase(db.get_db()).get_user_by_name(username)
        #name, email = FDataBase(db.get_db()).get_user_by_name(username)
        #title, body, url, created = FDataBase(db.get_db()).get_feedbacks_of_a_user(current_user.get_id())
        return render_template('profile.html') # feedbacks=feedbacks)

    def verify_ext(filename):
        """Verifies the extension of the file is 'png'"""
        ext = filename.rsplit('.', 1)[1]
        if ext == 'png' or ext == 'PNG':
            return True
        return False

    @app.route('/userava')
    @login_required
    def userava():
        """Returns an image in PNG-format"""
        dbase = get_db()
        user = dbase.execute('''SELECT * FROM users WHERE id = ?''', (session.get('user_id'),)).fetchone()
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
    @login_required
    def upload():
        """Uploads an image into user's profile"""
        dbase = get_db()
        user = dbase.execute('''SELECT * FROM users WHERE id = ?''', (session.get('user_id'),)).fetchone()
        if request.method == 'POST':
            file = request.files['file']
            if file and verify_ext(file.filename):
                try:
                    img = file.read()
                    dbase.execute(f'UPDATE users SET avatar = ? WHERE id = ?', (sqlite3.Binary(img), user['id']))
                    dbase.commit()
                except sqlite3.Error as e:
                    flash('Ошибка обновления аватара', 'error')
                except FileNotFoundError as e:
                    flash('Ошибка чтения файла', 'error')
            else:
                flash('Ошибка обновления аватара', 'error')
        flash('Аватар обновлен', 'success')
        return redirect(url_for('profile'))

    return app
