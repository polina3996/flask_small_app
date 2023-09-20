import pytest
from flask import session

from db import get_db
from FDataBase import FDataBase
from UserLogin import UserLogin


def test_fromDB(auth, client):
    auth.login()
    with client:
        client.get('/')
        assert UserLogin().fromDB(session['user_id'], FDataBase(get_db()))


def test_create(app):
    with app.app_context():
        user = FDataBase(get_db()).get_user_by_name(username='test_name')
        assert UserLogin().create(user)


@pytest.mark.parametrize('filename', ['test_filename.png', 'test_filename.PNG'])
def test_verify_ext(filename):
    assert UserLogin().verify_ext(filename)
    assert not UserLogin().verify_ext('test_filename.jpg')
