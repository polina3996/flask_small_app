import functools
from flask import Blueprint, request, g, redirect, url_for, flash, render_template, session
from flask_login import LoginManager, current_user, login_user, logout_user

from FDataBase import FDataBase
from UserLogin import UserLogin
from Forms import RegisterForm, LoginForm
from db import get_db
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint('auth', __name__)  # url_prefix='/auth'

# configures application for login
login_manager = LoginManager(auth)
# redirects to login page when trying to access must-be-authorized pages
login_manager.login_view = 'login'
login_manager.login_message = 'Авторизуйтесь для доступа к закрытым страницам'
login_manager.login_message_category = 'success'


@login_manager.user_loader
def load_user(user_id):
    """Reloads the user object from the user ID stored in the session"""
    return UserLogin().fromDB(user_id, FDataBase(get_db()))  # int(user_id)??


@auth.before_app_request
def load_logged_in_user():
    """Checking if there is a user in a session. If it is, user's data are collected from database and stored in a
    session (before each request!) """
    if session.get('user_id') is None:
        g.user = None
    else:
        g.user = get_db().execute('''SELECT * FROM users WHERE id = ?''', (session.get('user_id'),)).fetchone()


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page handler"""
    #if session.get('user_id'):
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # if request.method is POST
    form = RegisterForm()
    #db = get_db()

    if form.validate_on_submit():
        # try:
        #     db.cursor().execute('''INSERT INTO users VALUES (NULL, ?, ?, ?, NULL)''',
        #                         (form.username.data, form.email.data, hash,))
        #     db.commit()
        res = FDataBase(get_db()).add_user(form.username.data, form.email.data, generate_password_hash(form.psw.data))
        if res:
            flash('Вы успешно зарегистрированы', category='success')
            return redirect(url_for('auth.login'))
        # except db.IntegrityError:
        #     flash(f'Пользователь {form.username.data} уже зарегистрирован', category='error')
    # if request.method is GET or if there occurred some errors
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Authorization page handler"""
    # if session.get('user_id'):
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # if request.method is POST
    form = LoginForm()
    # db = get_db()

    if form.validate_on_submit():
        # user = db.execute('''SELECT * FROM users WHERE username = ?''', (form.username.data,)).fetchone()
        user = FDataBase(get_db()).get_user_by_name(form.username.data)
        if user and check_password_hash(user['password'], form.psw.data):
            session.clear()
            session['user_id'] = user['id']

            # registers the user as logged in, so that means that any future pages the user navigates to will have
            # the 'current_user' variable set to that user
            login_user(UserLogin().create(user), remember=form.remember.data)
            # next_page = request.args.get('next')
            #         if not next_page or url_parse(next_page).netloc != '':
            #             next_page = url_for('index')
            #         return redirect(next_page)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Неверная пара логин/пароль', category='error')
    # if request.method is GET or if there occurred some errors
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
def logout():
    """Logging out of session and deleting user's data"""
    # if not session.get('user_id'):
    #     return redirect(url_for('auth.login'))
    session.clear()
    logout_user()
    flash('Вы вышли из аккаунта', 'success')
    return redirect(url_for('index'))


# def login_required(view):
#     @functools.wraps(view)
#     def wrapped_view(**kwargs):
#         if g.user is None:
#             return redirect(url_for('auth.login'))
#         return view(**kwargs)
#
#     return wrapped_view
