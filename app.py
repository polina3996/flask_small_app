import os
from datetime import datetime
from flask import Flask, render_template, session, url_for, request, flash, redirect, g, make_response
from flask_login import LoginManager, current_user, login_required
import db
from FDataBase import FDataBase
from UserLogin import UserLogin
from instance.config import SECRET_KEY
from auth import auth as auth_bp
from feed import feed as feed_bp

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

    # registration of blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(feed_bp)

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

    @app.route('/restaurant/<rest_id>')
    def restaurant(rest_id):
        """Restaurant page handler"""
        rest_id, title, picture, url = FDataBase(db.get_db()).get_restaurant(rest_id)
        return render_template('rest.html', rest_id=rest_id, title=title, url=url)

    @app.route('/profile/<username>')  # just '/profile' -> page not found
    @login_required
    def profile(username):
        """Opens a profile page only for authorized users"""
        my_feedbacks = FDataBase(db.get_db()).get_feedbacks_of_a_user(g.user['id'])  # (current_user.get_id())
        return render_template('profile.html', my_feedbacks=my_feedbacks)

    @app.route('/userava')
    @login_required
    def userava():
        """Returns an image in PNG-format"""
        img = current_user.get_avatar(app)
        if not img:
            return ""
        h = make_response(img)
        h.headers['Content-Type'] = 'image/png'
        return h

    @app.route('/upload', methods=['POST', 'GET'])
    @login_required
    def upload():
        """Uploads an image into user's profile"""
        if request.method == 'POST':
            file = request.files['file']
            if file and current_user.verify_ext(file.filename):
                try:
                    img = file.read()
                    res = FDataBase(db.get_db()).update_user_avatar(img, session['user_id'])
                    if not res:
                        flash('Ошибка обновления аватара', 'error')
                    flash('Аватар обновлен', 'success')
                except FileNotFoundError as e:
                    flash('Ошибка чтения файла', 'error')
            else:
                flash('Ошибка обновления аватара', 'error')

        # after all + if it's GET-request
        return redirect(url_for('profile', username=g.user['username']))

    return app
