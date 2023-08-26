from flask import Flask, render_template
import os
from instance.config import SECRET_KEY


# вручную внести меню в БД или просписать в скл файле
# NAUmenu = ['Авторизация' blueprint_auth/login
#            'Регистрация' blueprint_auth/register
#            'Главная' /]
# AUmenu = [Имя blueprint_prof_feed/profile
#           Выйти blueprint_auth/logout
#           Главная /]

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

    @app.route('/')
    def index():
        return render_template('index.html')

    return app
