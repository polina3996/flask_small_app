import pytest
from flask import session, url_for

from FDataBase import FDataBase
from db import get_db


def test_object(app):
    with app.app_context():
        assert FDataBase(get_db()) is not None


@pytest.mark.parametrize('rest_id', [1, 2, 3, 4, 5, 6])
def test_get_restaurant(app, rest_id):
    with app.app_context():
        dbase = FDataBase(get_db())
        assert dbase.get_restaurant(rest_id)
        assert len(dbase.get_restaurant(rest_id)) == 3
        assert not dbase.get_restaurant(20)


@pytest.mark.parametrize(('username', 'email', 'hpsw'), (
        ('hdhf', 'testemail@gmail.com', 'a2a'),  # email already exists
        ('test_name', 'shd@dskd', 'a2a')  # username already exists
))
def test_add_false_user(app, username, email, hpsw):
    with app.app_context():
        dbase = FDataBase(get_db())
        assert not dbase.add_user(username, email, hpsw)


@pytest.mark.parametrize(('username', 'email', 'hpsw'), (
        ('hdhf', 'newemail@gmail.com', 'a2a'),
        ('new_name', 'shd@dskd', 'a2a')
))
def test_add_true_user(app, username, email, hpsw):
    with app.app_context():
        dbase = FDataBase(get_db())
        assert dbase.add_user(username, email, hpsw)
        assert dbase.get_user_by_name(username)


def test_get_user(client, username='test_name', email='test@gmail.com', hpsw='f2f'):
    with client:
        client.get('/')
        dbase = FDataBase(get_db())
        dbase.add_user(username, email, hpsw)
        assert dbase.get_user(1)


@pytest.mark.parametrize('username', ['test_name', 'test_username'])
def test_get_user_by_name(app, username):
    with app.app_context():
        dbase = FDataBase(get_db())
        assert dbase.get_user_by_name(username)
        assert len(dbase.get_user_by_name(username)) == 6


@pytest.mark.parametrize('rest_id', [1, 2, 3, 4, 5, 6])
def test_add_feedback(auth, client, rest_id, title='Test Feedback', body='This is a test feedback'):
    auth.login()
    with client:
        client.get('/')
        dbase = FDataBase(get_db())
        assert dbase.add_feedback(title, body, rest_id)


def test_get_feedbacks_of_a_user(auth, client, rest_id=1, title='Test Feedback', body='This is a test feedback'):
    auth.login()
    with client:
        client.get('/')
        dbase = FDataBase(get_db())
        dbase.add_feedback(title, body, rest_id)
        assert dbase.get_feedbacks_of_a_user('test_name') != []


def test_get_feedback(auth, client, rest_id=1, title='Test Feedback', body='This is a test feedback'):
    auth.login()
    with client:
        client.get('/')
        dbase = FDataBase(get_db())
        dbase.add_feedback(title, body, rest_id)
        assert dbase.get_feedback(1)


@pytest.mark.parametrize('rest_id', [1, 2, 3, 4, 5, 6])
def test_get_feedbacks_of_a_restaurant(auth, client, rest_id, title='Test Feedback', body='This is a test feedback'):
    auth.login()
    with client:
        client.get('/')
        dbase = FDataBase(get_db())
        dbase.add_feedback(title, body, rest_id)
        assert dbase.get_feedbacks_of_a_restaurant(rest_id) != []
        # assert dbase.get_feedback(1)['title'] == 'test title'
        # assert dbase.get_feedback(2)['title'] == 'Test Feedback'



def test_update_my_feedback(auth, client, feedback_id=1, new_title='New Title', new_body='This is a new body',
                            rest_id=1,
                            title='Test Feedback', body='This is a test feedback'):
    auth.login()
    with client:
        client.get('/')
        dbase = FDataBase(get_db())
        dbase.add_feedback(title, body, rest_id)
        assert dbase.update_my_feedback(feedback_id, new_title, new_body)
        assert dbase.get_feedback(feedback_id)['title'] == 'New Title'
        assert dbase.get_feedback(feedback_id)['body'] == 'This is a new body'


def test_delete_my_feedback(auth, client, feedback_id=1, rest_id=1, title='Test Feedback',
                            body='This is a test feedback'):
    auth.login()
    with client:
        client.get('/')
        dbase = FDataBase(get_db())
        dbase.add_feedback(title, body, rest_id)
        assert dbase.delete_my_feedback(feedback_id)
        assert not dbase.get_feedback(feedback_id)


def test_update_user_avatar(app, auth, client):
    auth.login()
    with client:
        client.get('/')
        dbase = FDataBase(get_db())
        with app.open_resource(app.root_path + url_for('static', filename='images/test.png'), 'rb') as f:
            img = f.read()
            assert dbase.update_user_avatar(avatar=img, user_id=session['user_id'])
            assert dbase.get_user(session['user_id'])['avatar']
