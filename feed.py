from flask import Blueprint, request, flash, render_template, redirect, url_for
from flask_login import login_required
from FDataBase import FDataBase
from db import get_db

feed = Blueprint('feed', __name__)


@feed.route('/leave_feedback', methods=['GET', 'POST'])
@login_required
def leave_feedback():
    """Leaving a feedback from an authorized current user to the chosen restaurant(the page visited before)"""
    if request.method == 'POST':
        if len(request.form['title']) > 4 and len(request.form['body']) > 10:
            res = FDataBase(get_db()).add_post(request.form['title'], request.form['body'])
            if not res:
                flash('Ошибка добавления отзыва', category='error')
            else:
                flash('Отзыв добавлен успешно', category='success')
                return redirect(url_for('index'))
        else:
            flash('Ошибка добавления отзыва', category='error')
    # if request method is 'GET'
    return render_template('feed/leave_feedback.html')

