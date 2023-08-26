import sqlite3
import click
from flask import current_app, g


def connect_db():
    """Connection to database"""
    conn = sqlite3.connect(current_app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    """Connect to the application's configured database. The connection
       is unique for each request and will be reused if this is called
       again.
       """
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db


def create_db():
    """Creating a database"""
    db = get_db()
    with current_app.open_resource('schema.sql', mode='r') as f:
        db.executescript(f.read())


def close_db(error=None):
    """If this request connected to the database, close the
            connection.
            """
    db = g.pop('db', None)
    if db is not None:
        db.close()


@click.command('init-db')
def init_db_command():
    """Deleting existing data and creating tables (with the message of success)"""
    create_db()
    click.echo('Создание базы данных')


def init_app(app):
    """Register database functions with the Flask app. This is called by
       the application factory.
       """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
