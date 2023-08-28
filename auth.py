from flask import Blueprint, request, g, redirect, url_for, flash, render_template
from Forms import RegisterForm
from db import get_db
from werkzeug.security import check_password_hash, generate_password_hash

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page handler"""
    if request.method == 'POST':
        form = RegisterForm()

        db = get_db()

        if form.validate_on_submit():
            hash = generate_password_hash(form.psw.data)
            try:
                db.execute('''INSERT INTO users VALUES (NULL, ?, ?, ?, NULL)''', (form.username.data, form.email.data, hash))
                db.commit()
                flash('Вы успешно зарегистрированы', category='success')
                return redirect(url_for('auth.login'))
            except db.IntegrityError:
                flash(f'Пользователь {form.username.data} уже зарегистрирован', category='error')
    # if request.method is GET or if there occurred some errors
    return render_template('auth/register.html')


