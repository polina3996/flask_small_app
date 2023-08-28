from flask import Blueprint, request, g, redirect, url_for, flash, render_template, session
from Forms import RegisterForm, LoginForm
from db import get_db
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint('auth', __name__)  # url_prefix='/auth'


@auth.before_app_request
def load_logged_in_user():
    """Checking if there is a user in a session. If it is, user's data are collected from database and stored in a
    session """
    if session.get('user_id') is None:
        g.user = None
    else:
        g.user = get_db().execute('''SELECT * FROM users WHERE id = ?''', (session.get('user_id'),)).fetchone()


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page handler"""
    form = RegisterForm()

    db = get_db()

    if form.validate_on_submit():
        hash = generate_password_hash(form.psw.data)
        try:
            db.execute('''INSERT INTO users VALUES (NULL, ?, ?, ?, NULL)''', (form.username.data, form.email.data, hash,))
            db.commit()
            flash('Вы успешно зарегистрированы', category='success')
            return redirect(url_for('auth.login'))
        except db.IntegrityError:
            flash(f'Пользователь {form.username.data} уже зарегистрирован', category='error')
    # if request.method is GET or if there occurred some errors
    return render_template('auth/register.html', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Authorization page handler"""
    if session.get('user_id'):
        return redirect(url_for('profile'))

    form = LoginForm()

    db = get_db()

    if form.validate_on_submit():
        user = db.execute('''SELECT * FROM users WHERE username = ?''', (form.username.data,)).fetchone()
        if user is not None and check_password_hash(user['password'], form.psw.data):
            session.clear()
            session['user_id'] = user['id']
            return redirect(request.args.get('next') or url_for('index'))
        flash('Неверная пара логин/пароль', category='error')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
def logout():
    """Logging out of session and deleting user's data"""
    if not session.get('user_id'):
        return redirect(url_for('auth.login'))
    session.clear()
    return redirect(url_for('index'))