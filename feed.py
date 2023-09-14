from flask import Blueprint, request, flash, render_template, redirect, url_for, g
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
            flash('Ошибка ввода отзыва, он слишком короткий', category='error')
    # if request method is 'GET'
    rest = FDataBase(get_db()).get_restaurant(rest_id)
    if rest:
        return render_template('feed/leave_feedback.html', rest_id=rest['id'], rest_title=rest['title'])
    # restaurant doesn't exist in the database
    else:
        return render_template('page404.html')


@feed.route('/feedback/<feedback_id>')
@login_required
def show_feedback(feedback_id):
    """Page where the full feedback s shown"""
    # only GET-request
    feedback = FDataBase(get_db()).get_feedback(feedback_id)
    # feedback doesn't exist in the database
    if feedback == ():
        return render_template('page404.html')
    return render_template('feed/feedback_rest.html', feedback_id=feedback_id, author=feedback['username'],
                           author_id=feedback['author_id'],
                           title=feedback['title'], body=feedback['body'], created=feedback['created'],
                           restaurant=feedback['restaurant'], rest_id=feedback['rest_id'])


@feed.route('/update_feedback/<feedback_id>', methods=['GET', 'POST'])
@login_required
def update_feedback(feedback_id):  # доб изменение времени создания отзыва?
    """Page where a user corrects his feedback"""
    if request.method == 'POST':
        if len(request.form['title']) > 4 and len(request.form['body']) > 10:
            res = FDataBase(get_db()).update_my_feedback(feedback_id, request.form['title'], request.form['body'])
            if not res:
                flash('Ошибка обновления отзыва', category='error')
            else:
                flash('Отзыв обновлен успешно', category='success')
                return redirect(url_for('feed.update_feedback', feedback_id=feedback_id))
    # GET-request
    feedback = FDataBase(get_db()).get_feedback(feedback_id)
    # feedback doesn't exist in the database OR it's not user's feedback
    if (feedback == ()) or (g.user['id'] != feedback['author_id']):
        return render_template('page404.html')
    return render_template('feed/update_feedback.html', title=feedback['title'], rest_title=feedback['restaurant'],
                           rest_id=feedback['rest_id'],
                           feedback_id=feedback_id, body=feedback['body'])


@feed.route('/delete_feedback/<feedback_id>', methods=['GET', 'POST'])
@login_required
def delete_feedback(feedback_id):
    """Page where a user deletes his feedback"""
    if request.method == 'POST':
        res = FDataBase(get_db()).delete_my_feedback(feedback_id)
        if res:
            flash('Отзыв удален успешно', category='success')
            return redirect(url_for('index'))
        else:
            flash('Ошибка удаления отзыва', category='error')
    # GET-request
    feedback = FDataBase(get_db()).get_feedback(feedback_id)
    # feedback doesn't exist in the database OR it's not user's feedback
    if (feedback == ()) or (g.user['id'] != feedback['author_id']):
        return render_template('page404.html')
    return render_template('feed/update_feedback.html', title=feedback['title'], rest_title=feedback['restaurant'],
                           rest_id=feedback['rest_id'],
                           feedback_id=feedback_id, body=feedback['body'])


@feed.route('/all_feedbacks/restaurant/<rest_id>')
@login_required
def all_feedbacks(rest_id):
    # only GET method
    restaurant = FDataBase(get_db()).get_restaurant(rest_id)
    feedbacks = FDataBase(get_db()).get_feedbacks_of_a_restaurant(rest_id)
    return render_template('feed/all_feedbacks.html', rest_id=rest_id, feedbacks=feedbacks, restaurant=restaurant['title'])
