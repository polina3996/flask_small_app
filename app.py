from flask import Flask, render_template, abort
import os
from FDataBase import FDataBase
from db import get_db
from instance.config import SECRET_KEY

#dbase = None


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY=SECRET_KEY, DATABASE=os.path.join(app.instance_path, 'flask_small_app.sqlite'))
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # @app.before_request
    # def before_request():
    #     """Catches the request and does the connection to database every time before each request"""
    #     global dbase
    #     db_con = get_db()
    #     dbase = FDataBase(db_con)

    @app.route('/')
    @app.route('/index')
    def index():
        """Main page handler"""
        return render_template('index.html')

    @app.route('/gourmand')
    def gourmand():
        """Restaurant 'Gourmand' page handler"""
        return render_template('gourmand.html')

    @app.route('/alaverdi')
    def alaverdi():
        """Restaurant 'Alaverdi' page handler"""
        return render_template('alaverdi.html')

    @app.route('/heart_of_batumi')
    def heart_of_batumi():
        """Restaurant 'Heart of Batumi' page handler"""
        return render_template('heart_of_batumi.html')

    @app.route('/panorama')
    def panorama():
        """Restaurant 'Panorama' page handler"""
        return render_template('panorama.html')

    @app.route('/tavaduri')
    def tavaduri():
        """Restaurant 'Tavaduri' page handler"""
        return render_template('tavaduri.html')

    @app.route('/mangal')
    def mangal():
        """Restaurant 'Mangal' page handler"""
        return render_template('mangal.html')

    # @app.route('/restaurant/<alias>')
    # def restaurant(alias):
    #     """Restaurant page handler"""
    #     title, url = dbase.get_restaurant(alias)
    #     if not title:
    #         abort(404)
    #     return render_template('restaurant.html', menu=dbase.get_menu(), title=title, post=post)

    import db
    db.init_app(app)

    return app
