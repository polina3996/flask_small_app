import sqlite3
import pytest

from db import get_db


def test_get_close_db(app):
    """Tests connection to database and closing it"""

    # test database connection must be the same as usual connection
    with app.app_context():
        db = get_db()
        assert db is get_db()

    # connection is closed after all
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')
    assert 'closed' in str(e.value)


def test_init_db_command(runner, monkeypatch):
    """Tests initializing the database and creating it"""

    class Recorder(object):
        # class that records what's been called
        called = False

    def fake_init_db():
        # records that create_db’s been called
        Recorder.called = True

    # monkeypatch fixture replaces the create_db function with one that records that it’s been called.
    monkeypatch.setattr('db.create_db', fake_init_db)

    # The runner fixture you wrote above is used to call the init-db command by name.
    # The init-db command should call the create_db function and output a message.
    result = runner.invoke(args=['init-db'])
    assert 'Создание базы данных\n' in result.output
    assert Recorder.called
