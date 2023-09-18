from flask import Blueprint, request, g, redirect, url_for, flash, render_template, session
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from FDataBase import FDataBase
from UserLogin import UserLogin
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
    # GET-request(logged in)
    if current_user.is_authenticated:
        return redirect(url_for('profile', username=g.user['username']))

    # POST-request(non logged in)
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']

        error = None

        if not username:
            error = 'Username is required'
        if not 4 <= len(username) <= 100:
            error = 'Name length should be from 4 to 100 symbols'
        if '@' not in email:
            error = 'Invalid email'
        if not password:
            error = 'Password is required'
        if not 4 <= len(password) <= 100:
            error = 'Password length should be from 4 to 100 symbols'
        if password != password2:
            error = "Passwords don't match"

        if error is None:
            res = FDataBase(get_db()).add_user(username, email, generate_password_hash(password))
            if res:
                flash('Вы успешно зарегистрированы', category='success')
                return redirect(url_for('auth.login'))
            else:
                flash('Это имя или почта уже заняты', category='error')
        else:
            flash(error, category='error')
    # error or GET-request(non logged in)
    return render_template('auth/register.html')

    # form = RegisterForm()
    #
    # if form.validate_on_submit():
    #     res = FDataBase(get_db()).add_user(form.username.data, form.email.data, generate_password_hash(form.psw.data))
    #     if res:
    #         flash('Вы успешно зарегистрированы', category='success')
    #         return redirect(url_for('auth.login'))
    #     else:
    #         flash('Это имя или почта уже заняты', category='error')
    # # error or GET-request(non logged in)
    # return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Authorization page handler"""
    if current_user.is_authenticated:
        return redirect(url_for('profile', username=g.user['username']))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None

        user = FDataBase(get_db()).get_user_by_name(username)
        if not user:
            error = 'Incorrect username.'
        if not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            login_user(UserLogin().create(user))
            flash(f'Добро пожаловать, {username}!', category='success')
            return redirect(request.args.get('next') or url_for('profile', username=user['username']))
        else:
            flash(error, category='error')
    return render_template('auth/login.html')

    #
    # # if request.method is POST
    # form = LoginForm()
    #
    # if form.validate_on_submit():
    #     user = FDataBase(get_db()).get_user_by_name(form.username.data)
    #     if not user:
    #         flash('Пользователь не найден', category='error')
    #         return render_template('auth/login.html', form=form)
    #     if user and check_password_hash(user['password'], form.psw.data):
    #         session.clear()
    #         session['user_id'] = user['id']
    #         login_user(UserLogin().create(user), remember=form.remember.data)
    #         flash(f'Добро пожаловать, {form.username.data}!', category='success')
    #         return redirect(request.args.get('next') or url_for('profile', username=user['username']))
    #     flash('Неверная пара логин/пароль', category='error')
    # # if request.method is GET or if there occurred some errors
    # return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    """Logging out of session and deleting user's data. If the user is not logged in, first send him to authorization"""
    session.clear()
    logout_user()
    flash('Вы вышли из аккаунта', 'success')
    return redirect(url_for('index'))
