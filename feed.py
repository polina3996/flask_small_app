from flask import Blueprint, request, flash, render_template, redirect, url_for
from flask_login import login_required
from FDataBase import FDataBase
from db import get_db

feed = Blueprint('feed', __name__)


@feed.route('/leave_feedback', methods=['GET', 'POST'])
@login_required
def leave_feedback():  # потом доб опцию что предложить ему рестораны на кот оставить отзыв он хочет
    """Leaving a feedback from an authorized current user to the chosen restaurant(the page visited before)"""
    if request.method == 'POST':
        rest_id = request.args.get('rest_id')

        if len(request.form['title']) > 4 and len(request.form['body']) > 10:
            res = FDataBase(get_db()).add_feedback(request.form['title'], request.form['body'], rest_id)
            if not res:
                flash('Ошибка добавления отзыва', category='error')
            else:
                flash('Отзыв добавлен успешно', category='success')
                return redirect(url_for('index'))
        else:
            flash('Ошибка добавления отзыва', category='error')
    # if request method is 'GET'
    return render_template('feed/leave_feedback.html')


@feed.route('/feedback/<feedback_id>')
@login_required
def show_feedback(feedback_id):
    """Page where the full feedback s shown"""
    author, restaurant, title, body, created = FDataBase(get_db()).get_feedback(feedback_id)
    return render_template('feed/show_feedback_rest.html', author=author, restaurant=restaurant, title=title, body=body, created=created)


