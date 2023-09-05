from flask import Blueprint, request, flash, render_template, redirect, url_for
from flask_login import login_required
from FDataBase import FDataBase
from db import get_db

feed = Blueprint('feed', __name__)


@feed.route('/leave_feedback/<rest_id>', methods=['GET', 'POST'])  # just '/leave_feedback' -> page not found
@login_required
def leave_feedback(rest_id):
    """Leaving a feedback from an authorized current user to the chosen restaurant(the page visited before)"""
    if request.method == 'POST':
        # rest_id = request.args.get('rest_id')
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
    rest_id, title, picture, url = FDataBase(get_db()).get_restaurant(rest_id)
    return render_template('feed/leave_feedback.html', rest_id=rest_id, rest_title=title, rest_url=url)


@feed.route('/feedback/<feedback_id>')
@login_required
def show_feedback(feedback_id):
    """Page where the full feedback s shown"""
    author, author_id, title, body, created, restaurant, rest_id = FDataBase(get_db()).get_feedback(feedback_id)
    return render_template('feed/feedback_rest.html', feedback_id=feedback_id, author=author, author_id=author_id, title=title, body=body, created=created, restaurant=restaurant, rest_id=rest_id)


@feed.route('/update_feedback/<feedback_id>', methods=['GET', 'POST'])
@login_required
def update_feedback(feedback_id): # доб изменение времени ?
    """Page where a user corrects his feedback"""
    author, author_id, title, body, created, restaurant, rest_id = FDataBase(get_db()).get_feedback(feedback_id)
    if request.method == 'POST':
        if len(request.form['title']) > 4 and len(request.form['body']) > 10:
            res = FDataBase(get_db()).update_my_feedback(feedback_id, request.form['title'], request.form['body'])
            if not res:
                flash('Ошибка обновления отзыва', category='error')
            else:
                flash('Отзыв обновлен успешно', category='success')
                return redirect(url_for('index'))
    # if request method is GET
    return render_template('feed/update_feedback.html', title=title, rest_title=restaurant, rest_id=rest_id, feedback_id=feedback_id, body=body)


@feed.route('/delete_feedback/<feedback_id>', methods=['GET', 'POST'])
@login_required
def delete_feedback(feedback_id):
    """Page where a user deletes his feedback"""
    author, author_id, title, body, created, restaurant, rest_id = FDataBase(get_db()).get_feedback(feedback_id)
    res = FDataBase(get_db()).delete_my_feedback(feedback_id)
    if res:
        flash('Отзыв удален успешно', category='success')
        return redirect(url_for('index'))
    else:
        flash('Ошибка удаления отзыва', category='error')
    return render_template('feed/update_feedback.html', title=title, rest_title=restaurant, rest_id=rest_id, feedback_id=feedback_id, body=body)


